import { ConfigTemplateItem } from '~/models/autoLabeling/template'

export interface TemplateRepository {
  list(projectId: string): Promise<string[]>

  find(projectId: string, optionName: string): Promise<ConfigTemplateItem>
}
