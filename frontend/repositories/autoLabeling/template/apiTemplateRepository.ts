import ApiService from '@/services/api.service'
import { TemplateRepository } from '~/domain/models/autoLabeling/templateRepository'
import { ConfigTemplateItem, ConfigResponse } from '~/domain/models/autoLabeling/template'

export class APITemplateRepository implements TemplateRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<string[]> {
    const url = `/projects/${projectId}/auto-labeling-templates`
    const response = await this.request.get(url)
    const responseItems: string[] = response.data
    return responseItems
  }

  async find(projectId: string, optionName: string): Promise<ConfigTemplateItem> {
    const url = `/projects/${projectId}/auto-labeling-templates/${optionName}`
    const response = await this.request.get(url)
    const responseItem: ConfigResponse = response.data
    return ConfigTemplateItem.valueOf(responseItem)
  }
}
