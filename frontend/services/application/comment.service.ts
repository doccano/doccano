import { CommentItem } from '@/models/comment'
import { CommentItemListRepository } from '@/repositories/comment/interface'

export class CommentReadDTO {
  id: number
  user: number
  username: string
  documentText: string
  text: string
  createdAt: string

  constructor(item: CommentItem) {
    this.id = item.id
    this.user = item.user
    this.username = item.username
    this.documentText = item.documentText
    this.text = item.text
    this.createdAt = item.createdAt
  }
}

export class CommentApplicationService {
  constructor(
    private readonly repository: CommentItemListRepository
  ) {}

  public async listProjectComment(projectId: string, q: string = ''): Promise<CommentReadDTO[]> {
    const items = await this.repository.listAll(projectId, q)
    return items.map(item => new CommentReadDTO(item))
  }

  public async list(projectId: string, docId: string): Promise<CommentReadDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map(item => new CommentReadDTO(item))
  }

  public create(projectId: string, docId: string, text: string): Promise<CommentItem> {
    return this.repository.create(projectId, docId, text)
  }

  public update(projectId: string, docId: string, item: CommentReadDTO): Promise<CommentItem> {
    const comment = new CommentItem(
      item.id, item.user, item.username, parseInt(docId), item.documentText, item.text, item.createdAt
    )
    return this.repository.update(projectId, docId, comment)
  }

  public delete(projectId: string, docId: string, item: CommentReadDTO): Promise<void> {
    return this.repository.delete(projectId, docId, item.id)
  }

  public deleteBulk(projectId: string, items: CommentReadDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.deleteBulk(projectId, ids)
  }
}
