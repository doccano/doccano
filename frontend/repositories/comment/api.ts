import ApiService from '@/services/api.service'
import { CommentItemList, CommentItem } from '@/models/comment'
import { CommentItemListRepository, CommentItemResponse } from './interface'

export class FromApiCommentItemListRepository implements CommentItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async listAll(projectId: string, q: string): Promise<CommentItemList> {
    const url = `/projects/${projectId}/comments?q=${q}`
    const response = await this.request.get(url)
    const items: CommentItemResponse[] = response.data
    return CommentItemList.valueOf(items.map(item => CommentItem.valueOf(item)))
  }

  async list(projectId: string, docId: string): Promise<CommentItemList> {
    const url = `/projects/${projectId}/docs/${docId}/comments`
    const response = await this.request.get(url)
    const items: CommentItemResponse[] = response.data
    return CommentItemList.valueOf(items.map(item => CommentItem.valueOf(item)))
  }

  async create(projectId: string, docId: string, text: string): Promise<CommentItem> {
    const url = `/projects/${projectId}/docs/${docId}/comments`
    const response = await this.request.post(url, { projectId, docId, text })
    const responseItem: CommentItemResponse = response.data
    return CommentItem.valueOf(responseItem)
  }

  async update(projectId: string, docId: string, item: CommentItem): Promise<CommentItem> {
    const url = `/projects/${projectId}/docs/${docId}/comments/${item.id}`
    const response = await this.request.put(url, item.toObject())
    const responseItem: CommentItemResponse = response.data
    return CommentItem.valueOf(responseItem)
  }

  async delete(projectId: string, docId: string, item: CommentItem): Promise<void> {
    const url = `/projects/${projectId}/docs/${docId}/comments/${item.id}`
    const response = await this.request.delete(url)
  }

  async deleteBulk(projectId: string, items: CommentItemList): Promise<void> {
    const url = `/projects/${projectId}/comments`
    await this.request.delete(url, { ids: items.ids() })
  }
}
