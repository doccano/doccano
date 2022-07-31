import ApiService from '@/services/api.service'
import { CommentRepository, SearchOption } from '@/domain/models/comment/commentRepository'
import { CommentItem, CommentItemList } from '@/domain/models/comment/comment'

function toModel(item: { [key: string]: any }): CommentItem {
  return new CommentItem(
    item.id,
    item.user,
    item.username,
    item.example,
    item.text,
    item.created_at
  )
}

function toPayload(item: CommentItem): { [key: string]: any } {
  return {
    id: item.id,
    user: item.user,
    text: item.text
  }
}

export class APICommentRepository implements CommentRepository {
  constructor(private readonly request = ApiService) {}

  async listAll(
    projectId: string,
    { limit = '10', offset = '0', q = '' }: SearchOption
  ): Promise<CommentItemList> {
    const url = `/projects/${projectId}/comments?q=${q}&limit=${limit}&offset=${offset}`
    const response = await this.request.get(url)
    return new CommentItemList(
      response.data.count,
      response.data.next,
      response.data.previous,
      response.data.results.map((item: { [key: string]: any }) => toModel(item))
    )
  }

  async list(projectId: string, exampleId: number): Promise<CommentItem[]> {
    const url = `/projects/${projectId}/comments?example=${exampleId}&limit=100`
    const response = await this.request.get(url)
    return response.data.results.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, exampleId: number, text: string): Promise<CommentItem> {
    const url = `/projects/${projectId}/comments?example=${exampleId}`
    const response = await this.request.post(url, {
      projectId,
      exampleId,
      text
    })
    return toModel(response.data)
  }

  async update(projectId: string, item: CommentItem): Promise<CommentItem> {
    const url = `/projects/${projectId}/comments/${item.id}`
    const payload = toPayload(item)
    const response = await this.request.put(url, payload)
    return toModel(response.data)
  }

  async delete(projectId: string, commentId: number): Promise<void> {
    const url = `/projects/${projectId}/comments/${commentId}`
    await this.request.delete(url)
  }

  async deleteBulk(projectId: string, items: number[]): Promise<void> {
    const url = `/projects/${projectId}/comments`
    await this.request.delete(url, { ids: items })
  }
}
