import ApiService from '@/services/api.service'
import { OptionsGroupItem } from '~/domain/models/perspective/question/question'

function toModel(item: { [key: string]: any }): OptionsGroupItem {
  return new OptionsGroupItem(item.id, item.name, item.options_questions)
}

function toPayload(item: OptionsGroupItem): { [key: string]: any } {
  return {
    id: item.id,
    name: item.name,
    options_questions: item.options_questions
  }
}

export class APIOptionsGroupRepository {
  constructor(private readonly baseUrl = 'option', private readonly request = ApiService) {}

  async create(projectId: string, item: OptionsGroupItem): Promise<OptionsGroupItem> {
    const url = `projects/${projectId}/${this.baseUrl}s-group/create`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async findByName(projectId: string, name: string): Promise<OptionsGroupItem> {
    const url = `projects/${projectId}/${this.baseUrl}s-group/${name}`
    const response = await this.request.get(url)
    return toModel(response.data)
  }
}
