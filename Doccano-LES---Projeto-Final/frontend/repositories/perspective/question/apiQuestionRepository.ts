import ApiService from '@/services/api.service'
import { QuestionItem } from '~/domain/models/perspective/question/question'

function toModel(item: { [key: string]: any }): QuestionItem {
  return new QuestionItem(
    item.id,
    item.question,
    item.type_id,
    item.answers,
    item.perspective_id ?? null,
    item.options_group ?? null
  )
}

export class APIQuestionRepository {
  constructor(private readonly baseUrl = 'question', private readonly request = ApiService) {}

  async create(projectId: string, item: QuestionItem): Promise<QuestionItem> {
    const url = `/projects/${projectId}/perspectives/${this.baseUrl}s/create`
    const payload = {
      question: item.question,
      type: item.type,
      answers: item.answers,
      perspective_id: item.perspective_id,
      options_group: item.options_group
    }
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async list(perspective_id: number, project_id: string): Promise<QuestionItem[]> {
    const url = `projects/${project_id}/perspectives/${perspective_id}/${this.baseUrl}s`

    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }
}
