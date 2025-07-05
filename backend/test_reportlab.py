#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o ReportLab está funcionando corretamente
"""

import sys
import os
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def test_reportlab():
    """Testa se o ReportLab está funcionando"""
    print("Testando ReportLab...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.units import inch
        
        print("✓ ReportLab importado com sucesso")
        
        # Testar criação de PDF simples
        import io
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.drawString(100, 750, "Test PDF - ReportLab is working!")
        p.showPage()
        p.save()
        
        pdf_data = buffer.getvalue()
        buffer.close()
        
        print(f"✓ PDF criado com sucesso - {len(pdf_data)} bytes")
        
        # Testar criação de PDF com platypus
        buffer2 = io.BytesIO()
        doc = SimpleDocTemplate(buffer2, pagesize=A4)
        
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph("Test Title", styles['Heading1']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Test content", styles['Normal']))
        
        # Testar tabela
        table_data = [['Header 1', 'Header 2'], ['Data 1', 'Data 2']]
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        doc.build(story)
        
        pdf_data2 = buffer2.getvalue()
        buffer2.close()
        
        print(f"✓ PDF com platypus criado com sucesso - {len(pdf_data2)} bytes")
        
        return True
        
    except ImportError as e:
        print(f"✗ Erro ao importar ReportLab: {e}")
        return False
    except Exception as e:
        print(f"✗ Erro ao criar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_project_data():
    """Testa se conseguimos acessar os dados do projeto"""
    print("\nTestando acesso aos dados do projeto...")
    
    try:
        from projects.models import Project
        
        # Buscar projeto de ID 18
        project = Project.objects.get(id=18)
        print(f"✓ Projeto encontrado: {project.name}")
        
        # Testar se temos dados para o relatório
        from projects.views.project import VersionsReport
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Criar request fake
        factory = RequestFactory()
        request = factory.get('/test/')
        request.user = User.objects.first()
        
        # Testar o relatório
        report_view = VersionsReport()
        report_view.kwargs = {'project_id': 18}
        response = report_view.get(request)
        
        print(f"✓ Relatório gerado com sucesso")
        print(f"  - Versões: {len(response.data.get('versions', []))}")
        print(f"  - Versão atual: {response.data.get('current_version', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar dados do projeto: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("TESTE DE DIAGNÓSTICO - REPORTLAB & PROJETO")
    print("=" * 50)
    
    success1 = test_reportlab()
    success2 = test_project_data()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✓ TODOS OS TESTES PASSARAM")
    else:
        print("✗ ALGUNS TESTES FALHARAM")
    print("=" * 50) 