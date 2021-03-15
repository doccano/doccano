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

  async list(projectId: string, docId: number): Promise<CommentItem[]> {
    const url = `/projects/${projectId}/docs/${docId}/comments`
    const response = await this.request.get(url)
    const items: CommentItemResponse[] = response.data
    return items.map(item => CommentItem.valueOf(item))
  }

  async create(projectId: string, docId: number, text: string): Promise<CommentItem> {
    const url = `/projects/${projectId}/docs/${docId}/comments`
    const response = await this.request.post(url, { projectId, docId, text })
    const responseItem: CommentItemResponse = response.data
    return CommentItem.valueOf(responseItem)
  }

  async update(projectId: string, docId: number, item: CommentItem): Promise<CommentItem> {
    const url = `/projects/${projectId}/docs/${docId}/comments/${item.id}`
    const response = await this.request.put(url, item.toObject())
    const responseItem: CommentItemResponse = response.data
    return CommentItem.valueOf(responseItem)
  }

  async delete(projectId: string, docId: number, commentId: number): Promise<void> {
    const url = `/projects/${projectId}/docs/${docId}/comments/${commentId}`
    const response = await this.request.delete(url)
  }

  async deleteBulk(projectId: string, items: number[]): Promise<void> {
    const url = `/projects/${projectId}/comments`
    await this.request.delete(url, { ids: items })
  }
}
