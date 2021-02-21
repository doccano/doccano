import ApiService from '@/services/api.service'
import { TemplateRepository } from '@/repositories/template/interface'
import { ConfigTemplateItem, ConfigResponse } from '@/models/config/config-template'

export class FromApiTemplateRepository implements TemplateRepository {
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
