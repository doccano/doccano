import ApiService from '@/services/api.service'
import { QuestionTypeItem } from '~/domain/models/perspective/question/question'

function toModel(item: { [key: string]: any }): QuestionTypeItem {
  return new QuestionTypeItem(item.id, item.question_type)
}

function toPayload(item: QuestionTypeItem): { [key: string]: any } {
  return {
    id: item.id,
    question_type: item.question_type
  }
}

export class APIQuestionTypeRepository {
  constructor(private readonly baseUrl = 'question', private readonly request = ApiService) {}

  async create(projectId: string, item: QuestionTypeItem): Promise<QuestionTypeItem> {
    const url = `projects/${projectId}/${this.baseUrl}-type/create`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async findById(projectId: string, id: number): Promise<QuestionTypeItem> {
    const url = `projects/${projectId}/${this.baseUrl}-type/${id}`
    const response = await this.request.get(url)
    return toModel(response.data)
  }
}
