from django.core.management.base import BaseCommand
from projects.models import ProjectVersion


class Command(BaseCommand):
    help = 'Salva snapshots históricos para versões existentes que não têm snapshots'

    def add_arguments(self, parser):
        parser.add_argument(
            '--project-id',
            type=int,
            help='ID do projeto específico para corrigir (opcional)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força recriação de snapshots mesmo se já existirem',
        )

    def handle(self, *args, **options):
        project_id = options.get('project_id')
        force = options.get('force', False)
        
        # Filtrar versões
        versions = ProjectVersion.objects.all().order_by('project_id', 'version')
        
        if project_id:
            versions = versions.filter(project_id=project_id)
            self.stdout.write(f"Processando versões do projeto {project_id}...")
        else:
            self.stdout.write("Processando todas as versões...")
        
        updated_count = 0
        error_count = 0
        
        for version in versions:
            try:
                # Verificar se precisa de snapshot
                if not version.examples_snapshot or force:
                    self.stdout.write(f"Criando snapshot para Projeto {version.project_id} - Versão {version.version}...")
                    
                    # Salvar snapshot
                    version.save_examples_snapshot()
                    updated_count += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Snapshot criado - {len(version.examples_snapshot)} exemplos"
                        )
                    )
                else:
                    self.stdout.write(f"Projeto {version.project_id} - Versão {version.version} já tem snapshot")
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Erro na Versão {version.version} do Projeto {version.project_id}: {str(e)}"
                    )
                )
        
        # Resultado final
        self.stdout.write("\n" + "="*50)
        self.stdout.write(f"SNAPSHOTS PROCESSADOS: {updated_count}")
        self.stdout.write(f"ERROS: {error_count}")
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {updated_count} snapshots criados com sucesso!"
                )
            )
        
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠ {error_count} erros encontrados"
                )
            )
        
        self.stdout.write("="*50) 