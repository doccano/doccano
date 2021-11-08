import ApiService from '@/services/api.service'
import { CommentRepository, CommentItemResponse } from '@/domain/models/comment/commentRepository'
import { CommentItem } from '~/domain/models/comment/comment'

export class APICommentRepository implements CommentRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async listAll(projectId: string, q: string): Promise<CommentItem[]> {
    const url = `/projects/${projectId}/comments?q=${q}`
    const response = await this.request.get(url)
    const items: CommentItemResponse[] = response.data
    return items.map(item => CommentItem.valueOf(item))
  }

  async list(projectId: string, exampleId: number): Promise<CommentItem[]> {
    const url = `/projects/${projectId}/examples/${exampleId}/comments`
    const response = await this.request.get(url)
    const items: CommentItemResponse[] = response.data
    return items.map(item => CommentItem.valueOf(item))
  }

  async create(projectId: string, exampleId: number, text: string): Promise<CommentItem> {
    const url = `/projects/${projectId}/examples/${exampleId}/comments`
    const response = await this.request.post(url, { projectId, exampleId, text })
    const responseItem: CommentItemResponse = response.data
    return CommentItem.valueOf(responseItem)
  }

  async update(projectId: string, exampleId: number, item: CommentItem): Promise<CommentItem> {
    const url = `/projects/${projectId}/examples/${exampleId}/comments/${item.id}`
    const response = await this.request.put(url, item.toObject())
    const responseItem: CommentItemResponse = response.data
    return CommentItem.valueOf(responseItem)
  }

  async delete(projectId: string, exampleId: number, commentId: number): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/comments/${commentId}`
    const response = await this.request.delete(url)
  }

  async deleteBulk(projectId: string, items: number[]): Promise<void> {
    const url = `/projects/${projectId}/comments`
    await this.request.delete(url, { ids: items })
  }
}
