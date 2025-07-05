from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from projects.models import Project
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly
from projects.serializers import ProjectPolymorphicSerializer, ProjectVersionSerializer


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectPolymorphicSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "description")
    ordering_fields = ["name", "created_at", "created_by", "project_type"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [IsAuthenticated & IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        return Project.objects.filter(role_mappings__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.add_admin()

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data["ids"]
        projects = Project.objects.filter(
            role_mappings__user=self.request.user,
            role_mappings__role__name=settings.ROLE_PROJECT_ADMIN,
            pk__in=delete_ids,
        )
        # Todo: I want to use bulk delete.
        # But it causes the constraint error.
        # See https://github.com/django-polymorphic/django-polymorphic/issues/229
        for project in projects:
            project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectPolymorphicSerializer
    lookup_url_kwarg = "project_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class CloneProject(views.APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        cloned_project = project.clone()
        serializer = ProjectPolymorphicSerializer(cloned_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CloseProject(views.APIView):
    """Fecha um projeto para discussão e votação de regras"""
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        try:
            project = get_object_or_404(Project, pk=self.kwargs["project_id"])
            
            # Verificar se o projeto pode ser fechado
            if project.status != 'open':
                return Response(
                    {"error": f"Project status is {project.status}. Only OPEN projects can be closed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Fechar o projeto
            project.close_project()
            
            return Response(
                {"message": "Project closed successfully", "current_version": project.current_version},
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback
            return Response(
                {"error": "Failed to close project", "details": str(e), "traceback": traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReopenProject(views.APIView):
    """Reabre um projeto numa nova versão"""
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        
        if project.reopen_project():
            serializer = ProjectPolymorphicSerializer(project)
            return Response({
                "message": f"Projeto reaberto na versão {project.current_version}",
                "project": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Projeto já está aberto"
            }, status=status.HTTP_400_BAD_REQUEST)


class ProjectVersionList(generics.ListAPIView):
    """Lista as versões de um projeto"""
    serializer_class = ProjectVersionSerializer
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Project.objects.get(pk=project_id).versions.all()


class ProjectVersionStatus(views.APIView):
    """Endpoint para verificar o status de versões e discrepâncias"""
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        
        # Informações básicas do projeto
        info = {
            "project_id": project.id,
            "project_name": project.name,
            "current_version": project.current_version,
            "status": project.status,
            "is_open": project.is_open,
            "is_closed": project.is_closed,
            "threshold": project.label_discrepancy_threshold,
        }
        
        # Se versão > 1, mostra estatísticas de discrepâncias
        if project.current_version > 1:
            discrepant_examples = project.get_discrepant_examples()
            info["discrepant_examples_count"] = len(discrepant_examples)
            info["discrepant_examples"] = discrepant_examples[:5]  # Mostra apenas os 5 primeiros
        
        # Histórico de versões
        versions = project.versions.all()
        info["versions_history"] = [
            {
                "version": v.version,
                "created_at": v.created_at,
                "created_by": v.created_by.username if v.created_by else None,
                "notes": v.notes
            }
            for v in versions
        ]
        
        return Response(info, status=status.HTTP_200_OK)


class DebugDiscrepancies(views.APIView):
    """Endpoint debug para verificar discrepâncias detalhadamente"""
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        
        from collections import defaultdict
        from examples.models import Example
        from labels.models import Category, Span
        
        # Pega apenas exemplos do projeto atual
        examples = Example.objects.filter(project=project)
        
        # Pega membros ativos do projeto
        active_user_ids = set(
            project.role_mappings.values_list('user_id', flat=True)
        )
        
        debug_info = {
            "project_id": project.id,
            "current_version": project.current_version,
            "total_examples": examples.count(),
            "active_users": list(active_user_ids),
            "examples_analysis": []
        }
        
        for example in examples[:10]:  # Analisa apenas os primeiros 10 exemplos
            # Pega usuários assignados a este exemplo específico
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )
            
            # Pega todas as anotações para este exemplo
            annotations_by_user = defaultdict(list)
            
            # Pega spans (apenas de usuários atribuídos a este exemplo)
            spans = Span.objects.filter(example=example).select_related('label', 'user')
            for span in spans:
                if span.user_id in assigned_user_ids:
                    label_text = span.label.text if span.label else 'No Label'
                    annotations_by_user[span.user_id].append({
                        'type': 'span',
                        'label': label_text,
                        'start': span.start_offset,
                        'end': span.end_offset
                    })
            
            # Pega categorias (apenas de usuários atribuídos a este exemplo)
            categories = Category.objects.filter(example=example).select_related('label', 'user')
            for category in categories:
                if category.user_id in assigned_user_ids:
                    label_text = category.label.text if category.label else 'No Label'
                    annotations_by_user[category.user_id].append({
                        'type': 'category',
                        'label': label_text
                    })
            
            # Análise de discrepâncias
            user_ids = list(annotations_by_user.keys())
            has_discrepancy = False
            discrepancy_details = []
            
            if len(user_ids) >= 2:
                # Verifica discrepâncias entre todos os pares de usuários
                for i in range(len(user_ids)):
                    for j in range(i + 1, len(user_ids)):
                        user1_annotations = annotations_by_user[user_ids[i]]
                        user2_annotations = annotations_by_user[user_ids[j]]
                        
                        if project._annotations_differ(user1_annotations, user2_annotations):
                            has_discrepancy = True
                            discrepancy_details.append({
                                "user1": user_ids[i],
                                "user2": user_ids[j],
                                "user1_annotations": user1_annotations,
                                "user2_annotations": user2_annotations
                            })
            
            # Determinar se este exemplo seria incluído na próxima versão
            would_be_included = False
            skip_reason = None
            
            if len(assigned_user_ids) < 2:
                skip_reason = "Less than 2 users assigned"
            elif has_discrepancy:
                would_be_included = True
            else:
                skip_reason = "No discrepancy"
            
            debug_info["examples_analysis"].append({
                "example_id": example.id,
                "example_text": example.text[:100] + "..." if len(example.text) > 100 else example.text,
                "assigned_users": list(assigned_user_ids),
                "confirmed_users": list(example.states.filter(confirmed_by_id__in=assigned_user_ids).values_list('confirmed_by_id', flat=True)),
                "is_fully_confirmed": len(set(example.states.filter(confirmed_by_id__in=assigned_user_ids).values_list('confirmed_by_id', flat=True))) == len(assigned_user_ids),
                "annotations_by_user": dict(annotations_by_user),
                "has_discrepancy": has_discrepancy,
                "discrepancy_details": discrepancy_details,
                "would_be_included_in_next_version": would_be_included,
                "skip_reason": skip_reason
            })
        
        return Response(debug_info, status=status.HTTP_200_OK)


class VersionsReport(views.APIView):
    """Relatório completo das versões do projeto"""
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        
        # Parâmetros de filtro
        version_filter = request.query_params.get('version', None)
        status_filter = request.query_params.get('status', None)  # 'discrepant' ou 'non_discrepant'
        user_filter = request.query_params.get('user', None)
        
        from collections import defaultdict
        from examples.models import Example
        from labels.models import Category, Span
        
        # Buscar todas as versões registadas
        registered_versions = project.versions.all().order_by('version')
        
        report_data = {
            "project_id": project.id,
            "project_name": project.name,
            "current_version": project.current_version,
            "threshold": project.label_discrepancy_threshold,
            "versions": []
        }
        
        # Sempre incluir Versão 1 (mesmo que não esteja registada)
        version_1_exists = registered_versions.filter(version=1).exists()
        
        if not version_1_exists:
            # Criar dados para Versão 1 virtual usando dados atuais (para backwards compatibility)
            version_1_data = {
                "version": 1,
                "created_at": project.created_at,
                "created_by": project.created_by.username if project.created_by else None,
                "notes": "Initial version",
                "examples": []
            }
            
            # Versão 1: todos os exemplos (dados atuais)
            example_ids = list(Example.objects.filter(project=project).values_list('id', flat=True))
            examples = Example.objects.filter(id__in=example_ids).select_related('project')
            
            # Membros ativos do projeto
            active_members = project.role_mappings.select_related('user').all()
            member_map = {m.user_id: m.user.username for m in active_members}
            
            for example in examples:
                # Calcular estatísticas para este exemplo usando dados atuais
                example_stats = self._calculate_example_stats(example, active_members, member_map)
                
                # Aplicar filtros
                if status_filter:
                    if status_filter == 'discrepant' and not example_stats['has_discrepancy']:
                        continue
                    if status_filter == 'non_discrepant' and example_stats['has_discrepancy']:
                        continue
                
                if user_filter:
                    user_id = int(user_filter)
                    if user_id not in example_stats['annotations_by_user']:
                        continue
                
                version_1_data["examples"].append(example_stats)
            
            # Aplicar filtro de versão
            if not version_filter or version_filter == '1':
                version_1_data["total_examples"] = len(version_1_data["examples"])
                version_1_data["discrepant_examples"] = len([e for e in version_1_data["examples"] if e['has_discrepancy']])
                version_1_data["non_discrepant_examples"] = len([e for e in version_1_data["examples"] if not e['has_discrepancy']])
                report_data["versions"].append(version_1_data)
        
        # Processar versões registadas usando snapshots históricos
        for version in registered_versions:
            version_data = {
                "version": version.version,
                "created_at": version.created_at,
                "created_by": version.created_by.username if version.created_by else None,
                "notes": version.notes,
                "examples": []
            }
            
            # Usar dados do snapshot histórico se disponível
            if version.examples_snapshot:
                # Usar dados históricos do snapshot
                for example_id_str, example_snapshot in version.examples_snapshot.items():
                    try:
                        # Aplicar filtros nos dados históricos
                        if status_filter:
                            if status_filter == 'discrepant' and not example_snapshot.get('has_discrepancy', False):
                                continue
                            if status_filter == 'non_discrepant' and example_snapshot.get('has_discrepancy', False):
                                continue
                        
                        if user_filter:
                            user_id = int(user_filter)
                            annotations_by_user = example_snapshot.get('annotations_by_user', {})
                            # Converter username de volta para user_id para filtro
                            active_members = project.role_mappings.select_related('user').all()
                            username_to_id = {m.user.username: m.user_id for m in active_members}
                            if user_id not in [username_to_id.get(username, 0) for username in annotations_by_user.keys()]:
                                continue
                        
                        version_data["examples"].append(example_snapshot)
                        
                    except (ValueError, KeyError):
                        # Se houver erro nos filtros, pular este exemplo
                        continue
            else:
                # Fallback para dados atuais (para versões criadas antes do snapshot)
                # Determinar quais exemplos estavam disponíveis nesta versão
                if version.version == 1:
                    # Versão 1: todos os exemplos
                    example_ids = list(Example.objects.filter(project=project).values_list('id', flat=True))
                else:
                    # Versão 2+: usar snapshot salvo ou dados atuais
                    example_ids = version.example_ids
                
                # Buscar exemplos desta versão
                examples = Example.objects.filter(id__in=example_ids).select_related('project')
                
                # Membros ativos do projeto
                active_members = project.role_mappings.select_related('user').all()
                member_map = {m.user_id: m.user.username for m in active_members}
                
                for example in examples:
                    # Calcular estatísticas para este exemplo usando dados atuais
                    example_stats = self._calculate_example_stats(example, active_members, member_map)
                    
                    # Aplicar filtros
                    if status_filter:
                        if status_filter == 'discrepant' and not example_stats['has_discrepancy']:
                            continue
                        if status_filter == 'non_discrepant' and example_stats['has_discrepancy']:
                            continue
                    
                    if user_filter:
                        user_id = int(user_filter)
                        if user_id not in example_stats['annotations_by_user']:
                            continue
                    
                    version_data["examples"].append(example_stats)
            
            # Aplicar filtro de versão
            if version_filter and str(version.version) != version_filter:
                continue
                
            version_data["total_examples"] = len(version_data["examples"])
            version_data["discrepant_examples"] = len([e for e in version_data["examples"] if e.get('has_discrepancy', False)])
            version_data["non_discrepant_examples"] = len([e for e in version_data["examples"] if not e.get('has_discrepancy', False)])
            
            report_data["versions"].append(version_data)
        
        # Ordenar versões por número
        report_data["versions"].sort(key=lambda x: x["version"])
        
        return Response(report_data, status=status.HTTP_200_OK)
    
    def _calculate_example_stats(self, example, active_members, member_map):
        """Calcula estatísticas detalhadas para um exemplo"""
        from collections import defaultdict
        from labels.models import Category, Span
        
        # Pegar usuários assignados a este exemplo
        assigned_user_ids = set(
            example.assignments.values_list('assignee_id', flat=True)
        )
        
        # Annotations por usuário
        annotations_by_user = defaultdict(list)
        
        # Spans
        spans = Span.objects.filter(example=example).select_related('label', 'user')
        for span in spans:
            if span.user_id in assigned_user_ids:
                label_text = span.label.text if span.label else 'No Label'
                annotations_by_user[span.user_id].append({
                    'type': 'span',
                    'label': label_text,
                    'start': span.start_offset,
                    'end': span.end_offset
                })
        
        # Categories
        categories = Category.objects.filter(example=example).select_related('label', 'user')
        for category in categories:
            if category.user_id in assigned_user_ids:
                label_text = category.label.text if category.label else 'No Label'
                annotations_by_user[category.user_id].append({
                    'type': 'category',
                    'label': label_text
                })
        
        # Calcular percentagens de labels
        label_counts = defaultdict(int)
        total_annotations = 0
        
        for user_id, annotations in annotations_by_user.items():
            for annotation in annotations:
                label_counts[annotation['label']] += 1
                total_annotations += 1
        
        # Calcular percentagens
        label_percentages = {}
        if total_annotations > 0:
            for label, count in label_counts.items():
                label_percentages[label] = {
                    'count': count,
                    'percentage': round((count / total_annotations) * 100, 1)
                }
        
        # Verificar discrepâncias baseadas no threshold
        has_discrepancy = False
        user_ids = list(annotations_by_user.keys())
        
        if len(user_ids) >= 2 and total_annotations > 0:
            # Calcular a maior percentagem de concordância
            max_percentage = 0
            if label_percentages:
                max_percentage = max(data['percentage'] for data in label_percentages.values())
            
            # Se a maior percentagem for menor que o threshold, é discrepante
            threshold = example.project.label_discrepancy_threshold
            has_discrepancy = max_percentage < threshold
        
        # Status do exemplo (confirmado ou não)
        confirmed_users = list(example.states.filter(
            confirmed_by_id__in=assigned_user_ids
        ).values_list('confirmed_by_id', flat=True))
        is_confirmed = len(confirmed_users) == len(assigned_user_ids)
        
        return {
            'example_id': example.id,
            'example_text': example.text,
            'assigned_users': [member_map.get(uid, f'User {uid}') for uid in assigned_user_ids],
            'confirmed_users': [member_map.get(uid, f'User {uid}') for uid in confirmed_users],
            'is_confirmed': is_confirmed,
            'has_discrepancy': has_discrepancy,
            'annotations_by_user': {
                member_map.get(uid, f'User {uid}'): annotations 
                for uid, annotations in annotations_by_user.items()
            },
            'label_percentages': label_percentages,
            'total_annotations': total_annotations,
            'status': 'Finished' if is_confirmed else 'In Progress'
        }


class VersionsReportExport(views.APIView):
    """Export do relatório de versões em CSV"""
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        
        # Reutilizar lógica do relatório
        report_view = VersionsReport()
        report_view.kwargs = self.kwargs
        report_response = report_view.get(request, *args, **kwargs)
        report_data = report_response.data
        
        # Criar CSV
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{project.name}_versions_report.csv"'
        
        writer = csv.writer(response)
        
        # Cabeçalhos
        writer.writerow([
            'Version', 'Example ID', 'Example Text', 'Status', 'Has Discrepancy',
            'Assigned Users', 'Confirmed Users', 'Total Annotations', 'Labels'
        ])
        
        # Dados
        for version in report_data['versions']:
            for example in version['examples']:
                labels_str = ', '.join([
                    f"{label}({data['percentage']}%)" 
                    for label, data in example['label_percentages'].items()
                ])
                
                assigned_users_str = ', '.join(example['assigned_users']) if example['assigned_users'] else ''
                confirmed_users_str = ', '.join(example['confirmed_users']) if example['confirmed_users'] else ''
                
                writer.writerow([
                    version['version'],
                    example['example_id'],
                    example['example_text'][:100] + '...' if len(example['example_text']) > 100 else example['example_text'],
                    example['status'],
                    'Yes' if example['has_discrepancy'] else 'No',
                    assigned_users_str,
                    confirmed_users_str,
                    example['total_annotations'],
                    labels_str
                ])
        
        return response


class TestPDFExport(views.APIView):
    """Endpoint de teste para verificar se o ReportLab está funcionando"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            from django.http import HttpResponse
            import io
            
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            
            # Criar PDF simples
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="test.pdf"'
            
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            p.drawString(100, 750, "Test PDF - ReportLab is working!")
            p.showPage()
            p.save()
            
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
            
        except Exception as e:
            import traceback
            from django.http import JsonResponse
            return JsonResponse({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)


class VersionsReportPDFExport(views.APIView):
    """Export do relatório de versões em PDF"""
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

    def get(self, request, *args, **kwargs):
        try:
            project = get_object_or_404(Project, pk=self.kwargs["project_id"])
            
            # Tentar gerar dados do relatório
            try:
                report_view = VersionsReport()
                report_view.kwargs = self.kwargs
                report_response = report_view.get(request, *args, **kwargs)
                report_data = report_response.data
            except Exception as e:
                # Se não conseguir gerar o relatório, retornar erro detalhado
                from django.http import JsonResponse
                return JsonResponse({
                    'error': 'Failed to generate report data',
                    'details': str(e)
                }, status=500)
            
            # Verificar se temos o ReportLab
            try:
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.units import inch
            except ImportError:
                # Fallback para HTML se não tiver ReportLab
                return self._generate_html_export(project, report_data)
            
            # Gerar PDF
            from django.http import HttpResponse
            import io
            
            response = HttpResponse(content_type='application/pdf')
            
            # Nome do arquivo seguro
            safe_name = "".join(c for c in str(project.name) if c.isalnum() or c in (' ', '-', '_')).strip()
            if not safe_name:
                safe_name = f"project_{project.id}"
            
            response['Content-Disposition'] = f'attachment; filename="{safe_name}_versions_report.pdf"'
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1
            )
            
            story = []
            
            # Título
            story.append(Paragraph(f"Versions Report - {safe_name}", title_style))
            story.append(Spacer(1, 12))
            
            # Informações do projeto
            current_version = report_data.get('current_version', 'N/A')
            threshold = report_data.get('threshold', 'N/A')
            versions_count = len(report_data.get('versions', []))
            
            project_info = f"""
            <b>Project:</b> {safe_name}<br/>
            <b>Current Version:</b> {current_version}<br/>
            <b>Threshold:</b> {threshold}%<br/>
            <b>Total Versions:</b> {versions_count}
            """
            story.append(Paragraph(project_info, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Processar versões
            versions = report_data.get('versions', [])
            
            if not versions:
                story.append(Paragraph("No versions found for this project.", styles['Normal']))
            else:
                for version_data in versions:
                    try:
                        # Dados da versão
                        version_num = str(version_data.get('version', 'Unknown'))
                        created_at = str(version_data.get('created_at', 'Unknown'))[:10]
                        created_by = str(version_data.get('created_by') or 'Unknown')
                        
                        # Título da versão
                        version_title = f"Version {version_num} - Created {created_at} by {created_by}"
                        story.append(Paragraph(version_title, styles['Heading2']))
                        
                        # Estatísticas
                        total_examples = version_data.get('total_examples', 0)
                        discrepant_examples = version_data.get('discrepant_examples', 0)
                        non_discrepant_examples = version_data.get('non_discrepant_examples', 0)
                        
                        stats = f"Examples: {total_examples} | Discrepant: {discrepant_examples} | Non-discrepant: {non_discrepant_examples}"
                        story.append(Paragraph(stats, styles['Normal']))
                        story.append(Spacer(1, 12))
                        
                        # Exemplos
                        examples = version_data.get('examples', [])
                        if examples:
                            # Criar tabela com validação robusta
                            table_data = [['ID', 'Text', 'Status', 'Discrepancy', 'Labels']]
                            
                            for example in examples:
                                try:
                                    # Validar e sanitizar dados
                                    example_id = str(example.get('example_id', 'N/A'))
                                    
                                    # Texto do exemplo
                                    example_text = str(example.get('example_text', 'N/A'))
                                    if len(example_text) > 80:
                                        example_text = example_text[:80] + '...'
                                    
                                    # Remover caracteres não-ASCII
                                    example_text = ''.join(c if ord(c) < 128 else '?' for c in example_text)
                                    
                                    status = str(example.get('status', 'N/A'))
                                    has_discrepancy = example.get('has_discrepancy', False)
                                    discrepancy_text = 'Yes' if has_discrepancy else 'No'
                                    
                                    # Labels com validação
                                    label_percentages = example.get('label_percentages', {})
                                    labels_list = []
                                    
                                    for label_name, label_info in label_percentages.items():
                                        try:
                                            if isinstance(label_info, dict):
                                                percentage = label_info.get('percentage', 0)
                                                labels_list.append(f"{label_name}({percentage}%)")
                                            else:
                                                labels_list.append(str(label_name))
                                        except:
                                            labels_list.append(str(label_name))
                                    
                                    labels_str = ', '.join(labels_list[:3])  # Máximo 3 labels
                                    if len(labels_list) > 3:
                                        labels_str += '...'
                                    
                                    if not labels_str:
                                        labels_str = 'No labels'
                                    
                                    table_data.append([
                                        example_id,
                                        example_text,
                                        status,
                                        discrepancy_text,
                                        labels_str
                                    ])
                                    
                                except Exception:
                                    # Se um exemplo falhar, adicionar linha de erro
                                    table_data.append(['Error', 'Failed to process example', 'N/A', 'N/A', 'N/A'])
                                    continue
                            
                            # Criar tabela se temos dados
                            if len(table_data) > 1:
                                try:
                                    table = Table(table_data, colWidths=[0.7*inch, 2.5*inch, 1*inch, 1*inch, 2.3*inch])
                                    table.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                        ('FONTSIZE', (0, 1), (-1, -1), 7),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ]))
                                    
                                    story.append(table)
                                except Exception:
                                    # Se a tabela falhar, adicionar lista simples
                                    story.append(Paragraph("Examples (table format failed):", styles['Heading3']))
                                    for i, row in enumerate(table_data[1:6]):  # Máximo 5 exemplos
                                        story.append(Paragraph(f"• ID {row[0]}: {row[1]} - {row[2]}", styles['Normal']))
                                    if len(table_data) > 6:
                                        story.append(Paragraph(f"... and {len(table_data) - 6} more examples", styles['Normal']))
                        else:
                            story.append(Paragraph("No examples in this version.", styles['Normal']))
                        
                        story.append(Spacer(1, 20))
                        
                    except Exception as e:
                        # Se uma versão falhar, adicionar erro e continuar
                        story.append(Paragraph(f"Error processing version: {str(e)}", styles['Normal']))
                        story.append(Spacer(1, 20))
                        continue
            
            # Gerar o PDF
            try:
                doc.build(story)
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
                return response
                
            except Exception as e:
                buffer.close()
                from django.http import JsonResponse
                return JsonResponse({
                    'error': 'Failed to generate PDF',
                    'details': str(e)
                }, status=500)
                
        except Exception as e:
            # Erro geral
            import traceback
            from django.http import JsonResponse
            return JsonResponse({
                'error': 'Unexpected error in PDF generation',
                'details': str(e),
                'traceback': traceback.format_exc()
            }, status=500)
    
    def _generate_html_export(self, project, report_data):
        """Fallback HTML export if reportlab is not available"""
        from django.http import HttpResponse
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Versions Report - {project.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; text-align: center; }}
                h2 {{ color: #666; border-bottom: 1px solid #ccc; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .stats {{ background-color: #f9f9f9; padding: 10px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>Versions Report - {project.name}</h1>
            <div class="stats">
                <p><strong>Current Version:</strong> {report_data['current_version']}</p>
                <p><strong>Threshold:</strong> {report_data['threshold']}%</p>
                <p><strong>Total Versions:</strong> {len(report_data['versions'])}</p>
            </div>
        """
        
        for version in report_data['versions']:
            html += f"""
            <h2>Version {version['version']} - {version['created_at'][:10]}</h2>
            <div class="stats">
                Examples: {version['total_examples']} | 
                Discrepant: {version['discrepant_examples']} | 
                Non-discrepant: {version['non_discrepant_examples']}
            </div>
            """
            
            if version['examples']:
                html += """
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Text</th>
                        <th>Status</th>
                        <th>Discrepancy</th>
                        <th>Labels</th>
                    </tr>
                """
                
                for example in version['examples']:
                    labels_str = ', '.join([
                        f"{label}({data['percentage']}%)" 
                        for label, data in example['label_percentages'].items()
                    ])
                    
                    html += f"""
                    <tr>
                        <td>{example['example_id']}</td>
                        <td>{example['example_text'][:100]}{'...' if len(example['example_text']) > 100 else ''}</td>
                        <td>{example['status']}</td>
                        <td>{'Yes' if example['has_discrepancy'] else 'No'}</td>
                        <td>{labels_str}</td>
                    </tr>
                    """
                
                html += "</table>"
            else:
                html += "<p>No examples in this version.</p>"
        
        html += "</body></html>"
        
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{project.name}_versions_report.html"'
        return response


class ProjectDebugStatus(views.APIView):
    """Debug endpoint para verificar status detalhado do projeto"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            project = get_object_or_404(Project, pk=self.kwargs["project_id"])
            
            # Informações detalhadas do projeto
            debug_info = {
                "project_id": project.id,
                "project_name": project.name,
                "current_status": project.status,
                "current_version": project.current_version,
                "created_at": project.created_at,
                "created_by": project.created_by.username if project.created_by else None,
                "can_close": project.status == 'open',
                "can_reopen": project.status == 'closed',
            }
            
            # Informações de versões
            versions = project.versions.all().order_by('version')
            debug_info["versions"] = []
            
            for version in versions:
                version_info = {
                    "version": version.version,
                    "created_at": version.created_at,
                    "example_ids_count": len(version.example_ids) if version.example_ids else 0,
                    "has_snapshot": bool(version.examples_snapshot),
                    "snapshot_examples_count": len(version.examples_snapshot) if version.examples_snapshot else 0
                }
                debug_info["versions"].append(version_info)
            
            return Response(debug_info, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            return Response({
                "error": str(e),
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
