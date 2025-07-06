import { APIPerspectiveRepository, CreateQuestionPayload, CreateAnswerPayload, QuestionListParams } from '@/repositories/perspective/apiPerspectiveRepository'
import { Question, Answer, ProjectStats } from '@/domain/models/perspective/question'

export class PerspectiveApplicationService {
  constructor(private readonly repository: APIPerspectiveRepository) {}

  // Questions
  async listQuestions(projectId: string, params: QuestionListParams = {}): Promise<Question[]> {
    return await this.repository.listQuestions(projectId, params)
  }

  async getQuestion(projectId: string, questionId: number): Promise<Question> {
    return await this.repository.getQuestion(projectId, questionId)
  }

  async createQuestion(projectId: string, payload: CreateQuestionPayload): Promise<Question> {
    return await this.repository.createQuestion(projectId, payload)
  }

  async updateQuestion(projectId: string, questionId: number, payload: Partial<CreateQuestionPayload>): Promise<Question> {
    return await this.repository.updateQuestion(projectId, questionId, payload)
  }

  async deleteQuestion(projectId: string, questionId: number): Promise<void> {
    return await this.repository.deleteQuestion(projectId, questionId)
  }

  async bulkCreateQuestions(projectId: string, questions: CreateQuestionPayload[]): Promise<Question[]> {
    return await this.repository.bulkCreateQuestions(projectId, questions)
  }

  async bulkDeleteQuestions(projectId: string, questionIds: number[]): Promise<void> {
    return await this.repository.bulkDeleteQuestions(projectId, questionIds)
  }

  async reorderAllQuestions(projectId: string): Promise<{ message: string; reordered_count: number }> {
    return await this.repository.reorderAllQuestions(projectId)
  }

  async deleteAllQuestions(projectId: string): Promise<void> {
    return await this.repository.deleteAllQuestions(projectId)
  }

  // Answers
  async listAnswers(projectId: string, questionId?: number): Promise<Answer[]> {
    return await this.repository.listAnswers(projectId, questionId)
  }

  async createAnswer(projectId: string, payload: CreateAnswerPayload): Promise<Answer> {
    return await this.repository.createAnswer(projectId, payload)
  }

  async deleteAnswer(projectId: string, answerId: number): Promise<void> {
    return await this.repository.deleteAnswer(projectId, answerId)
  }

  async getQuestionAnswers(projectId: string, questionId: number): Promise<any> {
    return await this.repository.getQuestionAnswers(projectId, questionId)
  }

  // Statistics
  async getProjectStats(projectId: string): Promise<ProjectStats> {
    return await this.repository.getProjectStats(projectId)
  }

  // Helper methods
  async getQuestionsForMember(projectId: string, memberId: number): Promise<Question[]> {
    return await this.listQuestions(projectId, { member_id: memberId })
  }

  async getUnansweredQuestions(projectId: string, memberId: number): Promise<Question[]> {
    return await this.listQuestions(projectId, { member_id: memberId, answered: false })
  }

  async getAnsweredQuestions(projectId: string, memberId: number): Promise<Question[]> {
    return await this.listQuestions(projectId, { member_id: memberId, answered: true })
  }
}
