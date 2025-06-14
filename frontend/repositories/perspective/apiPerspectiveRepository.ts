import ApiService from '@/services/api.service'
import { Question, Answer, QuestionOption, ProjectStats } from '@/domain/models/perspective/question'

function toQuestionOptionModel(item: { [key: string]: any }): QuestionOption {
  return new QuestionOption(
    item.id,
    item.text,
    item.order
  )
}

function toQuestionModel(item: { [key: string]: any }): Question {
  return new Question(
    item.id,
    item.text,
    item.question_type,
    item.is_required,
    item.order,
    item.options ? item.options.map(toQuestionOptionModel) : [],
    item.answer_count || 0,
    item.user_answered || false,
    item.created_at,
    item.updated_at
  )
}

function toAnswerModel(item: { [key: string]: any }): Answer {
  return new Answer(
    item.id,
    item.question,
    item.text_answer,
    item.selected_option,
    item.created_at
  )
}

function toProjectStatsModel(item: { [key: string]: any }): ProjectStats {
  return new ProjectStats(
    item.total_questions,
    item.total_answers,
    item.questions_with_answers,
    item.questions || []
  )
}

export interface CreateQuestionPayload {
  text: string
  question_type: string
  is_required: boolean
  order: number
  options?: { text: string; order: number }[]
}

export interface CreateAnswerPayload {
  question: number
  text_answer?: string
  selected_option?: number
}

export interface QuestionListParams {
  member_id?: number
  answered?: boolean
  question_type?: string
  is_required?: boolean
  ordering?: string
}

export class APIPerspectiveRepository {
  constructor(private readonly request = ApiService) {}

  // Questions
  async listQuestions(projectId: string, params: QuestionListParams = {}): Promise<Question[]> {
    const queryParams = new URLSearchParams()

    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        queryParams.append(key, value.toString())
      }
    })

    const queryString = queryParams.toString()
    const url = `/projects/${projectId}/perspective/questions/${queryString ? '?' + queryString : ''}`
    console.log('Making request to:', url)

    const response = await this.request.get(url)
    console.log('API Response:', response)
    console.log('Response data:', response.data)

    // Handle different response formats
    const data = response.data
    if (Array.isArray(data)) {
      return data.map(toQuestionModel)
    } else if (data && Array.isArray(data.results)) {
      // Paginated response
      return data.results.map(toQuestionModel)
    } else {
      console.error('Unexpected response format:', data)
      return []
    }
  }

  async getQuestion(projectId: string, questionId: number): Promise<Question> {
    const url = `/projects/${projectId}/perspective/questions/${questionId}/`
    const response = await this.request.get(url)
    return toQuestionModel(response.data)
  }

  async createQuestion(projectId: string, payload: CreateQuestionPayload): Promise<Question> {
    const url = `/projects/${projectId}/perspective/questions/`
    const response = await this.request.post(url, payload)
    return toQuestionModel(response.data)
  }

  async updateQuestion(projectId: string, questionId: number, payload: Partial<CreateQuestionPayload>): Promise<Question> {
    const url = `/projects/${projectId}/perspective/questions/${questionId}/`
    const response = await this.request.patch(url, payload)
    return toQuestionModel(response.data)
  }

  async deleteQuestion(projectId: string, questionId: number): Promise<void> {
    const url = `/projects/${projectId}/perspective/questions/${questionId}/`
    await this.request.delete(url)
  }

  async bulkCreateQuestions(projectId: string, questions: CreateQuestionPayload[]): Promise<Question[]> {
    const url = `/projects/${projectId}/perspective/questions/bulk_create/`
    const response = await this.request.post(url, { questions })
    return response.data.map(toQuestionModel)
  }

  async bulkDeleteQuestions(projectId: string, questionIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/perspective/questions/bulk_delete/`
    await this.request.post(url, { question_ids: questionIds })
  }

  // Answers
  async listAnswers(projectId: string, questionId?: number): Promise<Answer[]> {
    const params = questionId ? `?question=${questionId}` : ''
    const url = `/projects/${projectId}/perspective/answers/${params}`
    const response = await this.request.get(url)

    // Handle different response formats
    const data = response.data
    if (Array.isArray(data)) {
      return data.map(toAnswerModel)
    } else if (data && Array.isArray(data.results)) {
      // Paginated response
      return data.results.map(toAnswerModel)
    } else {
      console.error('Unexpected response format:', data)
      return []
    }
  }

  async createAnswer(projectId: string, payload: CreateAnswerPayload): Promise<Answer> {
    const url = `/projects/${projectId}/perspective/answers/`
    const response = await this.request.post(url, payload)
    return toAnswerModel(response.data)
  }

  // Statistics
  async getProjectStats(projectId: string): Promise<ProjectStats> {
    const url = `/projects/${projectId}/perspective/stats/`
    const response = await this.request.get(url)
    return toProjectStatsModel(response.data)
  }
}
