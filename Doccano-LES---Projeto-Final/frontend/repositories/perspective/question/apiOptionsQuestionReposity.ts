import ApiService from '@/services/api.service'
import { OptionsQuestionItem } from '~/domain/models/perspective/question/question'

function toModel(item: { [key: string]: any }): OptionsQuestionItem {
  return new OptionsQuestionItem(item.id, item.option, item.options_group)
}

function toPayload(item: OptionsQuestionItem): { [key: string]: any } {
  return {
    id: item.id,
    option: item.option,
    options_group: item.options_group
  }
}

export class APIOptionsQuestionRepository {
  constructor(private readonly baseUrl = 'question', private readonly request = ApiService) {}

  async create(projectId: string, item: OptionsQuestionItem): Promise<OptionsQuestionItem> {
      const url = `projects/${projectId}/perspectives//${this.baseUrl}-type/create`
      const payload = toPayload(item)
      const response = await this.request.post(url, payload)
      return toModel(response.data)
    }

  async list(project_id: string): Promise<OptionsQuestionItem[]> {
    const url = `projects/${project_id}/options-${this.baseUrl}s`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }
}
