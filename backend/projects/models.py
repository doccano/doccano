import abc
import uuid
from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager
from polymorphic.models import PolymorphicModel

from roles.models import Role


class ProjectType(models.TextChoices):
    DOCUMENT_CLASSIFICATION = "DocumentClassification"
    SEQUENCE_LABELING = "SequenceLabeling"
    SEQ2SEQ = "Seq2seq"
    INTENT_DETECTION_AND_SLOT_FILLING = "IntentDetectionAndSlotFilling"
    SPEECH2TEXT = "Speech2text"
    IMAGE_CLASSIFICATION = "ImageClassification"
    BOUNDING_BOX = "BoundingBox"
    SEGMENTATION = "Segmentation"
    IMAGE_CAPTIONING = "ImageCaptioning"


class ProjectStatus(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Project(PolymorphicModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    guideline = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    project_type = models.CharField(max_length=30, choices=ProjectType.choices)
    random_order = models.BooleanField(default=False)
    collaborative_annotation = models.BooleanField(default=False)
    single_class_classification = models.BooleanField(default=False)
    allow_member_to_create_label_type = models.BooleanField(default=False)
    label_discrepancy_threshold = models.FloatField(
        default=0.0,
        help_text="Percentagem mínima de discrepância de labels (0-100)"
    )
    status = models.CharField(
        max_length=10,
        choices=ProjectStatus.choices,
        default=ProjectStatus.OPEN,
        help_text="Estado do projeto para controle de versões"
    )
    current_version = models.PositiveIntegerField(
        default=1,
        help_text="Versão atual do projeto"
    )

    def add_admin(self):
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        Member.objects.create(
            project=self,
            user=self.created_by,
            role=admin_role,
        )

    def close_project(self):
        """Fecha o projeto para discussão e votação"""
        if self.status != 'open':
            raise ValueError("Projeto deve estar aberto para ser fechado")
        
        self.status = 'closed'
        
        try:
            # Verificar se existe uma versão atual
            current_version_obj = self.versions.filter(version=self.current_version).first()
            
            if not current_version_obj:
                # Se não existe versão registada, criar uma para a versão atual
                from examples.models import Example
                example_ids = list(Example.objects.filter(project=self).values_list('id', flat=True))
                
                current_version_obj = ProjectVersion.objects.create(
                    project=self,
                    version=self.current_version,
                    created_by=self.created_by,
                    example_ids=example_ids,
                    notes=f"Version {self.current_version} - Auto-created when closing project"
                )
            
            # Salvar snapshot se ainda não foi salvo
            if not current_version_obj.examples_snapshot:
                current_version_obj.save_examples_snapshot()
                
        except Exception as e:
            # Se falhar ao criar snapshot, ainda assim fechar o projeto
            # O snapshot pode ser criado posteriormente se necessário
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create snapshot for project {self.id} version {self.current_version}: {str(e)}")
        
        self.save()
        return True

    def reopen_project(self):
        """Reabre o projeto numa nova versão"""
        if self.status != 'closed':
            raise ValueError("Projeto deve estar fechado para ser reaberto")
        
        # Salvar snapshot da versão atual antes de criar nova versão
        current_version_obj = self.versions.filter(version=self.current_version).first()
        if current_version_obj and not current_version_obj.examples_snapshot:
            current_version_obj.save_examples_snapshot()
        
        # Incrementar versão
        self.current_version += 1
        self.status = 'open'
        
        # Criar nova versão com exemplos discrepantes
        discrepant_examples = self.get_discrepant_examples()
        example_ids = [ex.id for ex in discrepant_examples]
        
        new_version = ProjectVersion.objects.create(
            project=self,
            version=self.current_version,
            example_ids=example_ids,
            notes=f"Version {self.current_version} - Discrepant examples from previous version"
        )
        
        # NÃO criar snapshot aqui - será criado quando o projeto for fechado
        
        self.save()
        return new_version

    def get_version_examples(self):
        """Retorna os IDs dos exemplos que devem ser mostrados na versão atual"""
        if self.current_version == 1:
            # Versão 1: todos os exemplos
            from examples.models import Example
            return list(Example.objects.filter(project=self).values_list('id', flat=True))
        else:
            # Versão 2+: usa o snapshot salvo na criação da versão
            try:
                version = self.versions.get(version=self.current_version)
                return version.example_ids
            except ProjectVersion.DoesNotExist:
                # Fallback: recalcula se não encontrar a versão
                return self.get_discrepant_examples()

    def get_discrepant_examples(self):
        """Retorna exemplos que têm discrepâncias baseadas no threshold"""
        from collections import defaultdict
        from examples.models import Example
        from labels.models import Category, Span
        
        # Pega apenas exemplos do projeto atual
        examples = Example.objects.filter(project=self)
        
        # Pega membros ativos do projeto
        active_user_ids = set(
            self.role_mappings.values_list('user_id', flat=True)
        )
        
        discrepant_example_ids = []
        
        for example in examples:
            # Pega usuários assignados a este exemplo específico
            assigned_user_ids = set(
                example.assignments.filter(assignee_id__in=active_user_ids).values_list('assignee_id', flat=True)
            )
            
            # Pula exemplos com menos de 2 usuários atribuídos
            if len(assigned_user_ids) < 2:
                continue
                
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
            
            # Apenas analisa exemplos que têm anotações de múltiplos usuários
            user_ids = list(annotations_by_user.keys())
            if len(user_ids) >= 2:
                # Verifica discrepâncias entre todos os pares de usuários
                has_discrepancy = False
                
                for i in range(len(user_ids)):
                    for j in range(i + 1, len(user_ids)):
                        user1_annotations = annotations_by_user[user_ids[i]]
                        user2_annotations = annotations_by_user[user_ids[j]]
                        
                        if self._annotations_differ(user1_annotations, user2_annotations):
                            has_discrepancy = True
                            break
                    if has_discrepancy:
                        break
                
                if has_discrepancy:
                    discrepant_example_ids.append(example.id)
        
        return [Example.objects.get(id=ex_id) for ex_id in discrepant_example_ids]

    def _annotations_differ(self, annotations1, annotations2):
        """Compara dois conjuntos de anotações para detectar discrepâncias"""
        # Converte anotações para formato comparável
        set1 = set()
        set2 = set()
        
        for ann in annotations1:
            if ann['type'] == 'span':
                set1.add((ann['label'], ann['start'], ann['end']))
            else:
                set1.add((ann['label'],))
        
        for ann in annotations2:
            if ann['type'] == 'span':
                set2.add((ann['label'], ann['start'], ann['end']))
            else:
                set2.add((ann['label'],))
        
        return set1 != set2

    @property
    def is_open(self):
        return self.status == ProjectStatus.OPEN

    @property
    def is_closed(self):
        return self.status == ProjectStatus.CLOSED

    @property
    @abc.abstractmethod
    def is_text_project(self) -> bool:
        return False

    def clone(self) -> "Project":
        """Clone the project.
        See https://docs.djangoproject.com/en/4.2/topics/db/queries/#copying-model-instances

        Returns:
            The cloned project.
        """
        project = Project.objects.get(pk=self.pk)
        project.pk = None
        project.id = None
        project._state.adding = True
        project.save()

        def bulk_clone(queryset: models.QuerySet, field_initializers: Optional[Dict[Any, Any]] = None):
            """Clone the queryset.

            Args:
                queryset: The queryset to clone.
                field_initializers: The field initializers.
            """
            if field_initializers is None:
                field_initializers = {}
            items = []
            for item in queryset:
                item.id = None
                item.pk = None
                for field, value_or_callable in field_initializers.items():
                    if callable(value_or_callable):
                        value_or_callable = value_or_callable()
                    setattr(item, field, value_or_callable)
                item.project = project
                item._state.adding = True
                items.append(item)
            queryset.model.objects.bulk_create(items)

        bulk_clone(self.role_mappings.all())
        bulk_clone(self.tags.all())

        # clone examples
        bulk_clone(self.examples.all(), field_initializers={"uuid": uuid.uuid4})

        # clone label types
        bulk_clone(self.categorytype_set.all())
        bulk_clone(self.spantype_set.all())
        bulk_clone(self.relationtype_set.all())

        return project

    def __str__(self):
        return self.name


class TextClassificationProject(Project):
    @property
    def is_text_project(self) -> bool:
        return True


class SequenceLabelingProject(Project):
    allow_overlapping = models.BooleanField(default=False)
    grapheme_mode = models.BooleanField(default=False)
    use_relation = models.BooleanField(default=False)

    @property
    def is_text_project(self) -> bool:
        return True


class Seq2seqProject(Project):
    @property
    def is_text_project(self) -> bool:
        return True


class IntentDetectionAndSlotFillingProject(Project):
    @property
    def is_text_project(self) -> bool:
        return True


class Speech2textProject(Project):
    @property
    def is_text_project(self) -> bool:
        return False


class ImageClassificationProject(Project):
    @property
    def is_text_project(self) -> bool:
        return False


class BoundingBoxProject(Project):
    @property
    def is_text_project(self) -> bool:
        return False


class SegmentationProject(Project):
    @property
    def is_text_project(self) -> bool:
        return False


class ImageCaptioningProject(Project):
    @property
    def is_text_project(self) -> bool:
        return False


class Tag(models.Model):
    text = models.TextField()
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.text


class MemberManager(Manager):
    def can_update(self, project: int, member_id: int, new_role: str) -> bool:
        """The project needs at least 1 admin.

        Args:
            project: The project id.
            member_id: The member id.
            new_role: The new role name.

        Returns:
            Whether the mapping can be updated or not.
        """
        queryset = self.filter(project=project, role__name=settings.ROLE_PROJECT_ADMIN)
        if queryset.count() > 1:
            return True
        else:
            admin = queryset.first()
            # we can change the role except for the only admin.
            return admin.id != member_id or new_role == settings.ROLE_PROJECT_ADMIN

    def has_role(self, project_id: int, user: User, role_name: str):
        return self.filter(project=project_id, user=user, role__name=role_name).exists()


class Member(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="role_mappings")
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="role_mappings")
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MemberManager()

    def clean(self):
        members = self.__class__.objects.exclude(id=self.id)
        if members.filter(user=self.user, project=self.project).exists():
            message = "This user is already assigned to a role in this project."
            raise ValidationError(message)

    def is_admin(self):
        return self.role.name == settings.ROLE_PROJECT_ADMIN

    @property
    def username(self):
        return self.user.username

    class Meta:
        unique_together = ("user", "project")


class ProjectVersion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='versions')
    version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    
    # IDs dos exemplos desta versão
    example_ids = models.JSONField(default=list, blank=True)
    
    # Snapshot histórico dos dados dos exemplos nesta versão
    examples_snapshot = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ('project', 'version')
        ordering = ['version']

    def __str__(self):
        return f"{self.project.name} - Version {self.version}"
    
    def save_examples_snapshot(self):
        """Salva o snapshot dos dados dos exemplos no momento da criação da versão"""
        from collections import defaultdict
        from labels.models import Category, Span
        from examples.models import Example
        
        try:
            snapshot = {}
            
            # Buscar exemplos desta versão
            if self.example_ids:
                examples = Example.objects.filter(id__in=self.example_ids).select_related('project')
            else:
                # Se não há IDs específicos, buscar todos os exemplos do projeto
                examples = Example.objects.filter(project=self.project).select_related('project')
            
            # Membros ativos do projeto
            active_members = self.project.role_mappings.select_related('user').all()
            member_map = {m.user_id: m.user.username for m in active_members}
            
            for example in examples:
                try:
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
                    
                    # Salvar snapshot do exemplo
                    snapshot[str(example.id)] = {
                        'example_id': example.id,
                        'example_text': example.text or '',
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
                        'status': 'Finished' if is_confirmed else 'In Progress',
                        'snapshot_date': self.created_at.isoformat() if self.created_at else None
                    }
                    
                except Exception as e:
                    # Se um exemplo falhar, continuar com os outros
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to create snapshot for example {example.id}: {str(e)}")
                    continue
            
            self.examples_snapshot = snapshot
            self.save(update_fields=['examples_snapshot'])
            
        except Exception as e:
            # Se todo o processo falhar, re-raise a exception
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create examples snapshot for version {self.id}: {str(e)}")
            raise
