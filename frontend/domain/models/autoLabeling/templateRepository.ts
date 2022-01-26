import { ConfigTemplateItem } from '~/domain/models/autoLabeling/template'

export interface TemplateRepository {
  list(projectId: string, taskName: string): Promise<string[]>

  find(projectId: string, optionName: string): Promise<ConfigTemplateItem>
}
