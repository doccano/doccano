import ApiService from '@/services/api.service'
import { AnswerItem } from '~/domain/models/perspective/answer/answer'

function toModel(item: { [key: string]: any }): AnswerItem {
  return new AnswerItem(item.id,item.member, item.question, item.answer_text, item.answer_option)
}

function toPayload(item: AnswerItem): { [key: string]: any } {
  return {
    id: item.id,
    member: item.member,
    question: item.question,
    answer_text: item.answer_text,
    answer_option: item.answer_option
  }
}

export class APIAnswerRepository {
  constructor(private readonly baseUrl = 'answer', private readonly request = ApiService) {}

  async list(username?: string): Promise<AnswerItem[]> {
    let url = `/${this.baseUrl}s`

    if (username) {
      url += `?search=${encodeURIComponent(username)}`
    }

    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, item: AnswerItem): Promise<AnswerItem> {
    const url = `/projects/${projectId}/perspectives/${this.baseUrl}s/create`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }
}
