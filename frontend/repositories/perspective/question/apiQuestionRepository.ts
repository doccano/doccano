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

  async list(perspectiveId: string, project_id: string): Promise<QuestionItem[]> {
    const url = `projects/${project_id}/perspectives/${perspectiveId}/${this.baseUrl}s`

    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }
}
