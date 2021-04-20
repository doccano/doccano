import { TemplateRepository } from '~/domain/models/autoLabeling/templateRepository'
import { ConfigTemplateItem } from '~/domain/models/autoLabeling/template'

export class TemplateApplicationService {
  constructor(
    private readonly repository: TemplateRepository
  ) {}

  public list(id: string): Promise<string[]> {
    return this.repository.list(id)
  }

  public find(projectId: string, optionName: string): Promise<ConfigTemplateItem> {
    return this.repository.find(projectId, optionName)
  }
}
