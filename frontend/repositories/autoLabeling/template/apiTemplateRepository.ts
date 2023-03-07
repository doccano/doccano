import ApiService from '@/services/api.service'
import { ConfigResponse, ConfigTemplateItem } from '~/domain/models/autoLabeling/template'

export class APITemplateRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: string, taskName: string): Promise<string[]> {
    const url = `/projects/${projectId}/auto-labeling/templates?task_name=${taskName}`
    const response = await this.request.get(url)
    const responseItems: string[] = response.data
    return responseItems
  }

  async find(projectId: string, optionName: string): Promise<ConfigTemplateItem> {
    const url = `/projects/${projectId}/auto-labeling/templates/${optionName}`
    const response = await this.request.get(url)
    const responseItem: ConfigResponse = response.data
    return ConfigTemplateItem.valueOf(responseItem)
  }
}
