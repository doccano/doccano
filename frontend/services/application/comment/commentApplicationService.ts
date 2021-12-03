import { CommentReadDTO, CommentListDTO } from './commentData'
import { CommentRepository, SearchOption } from '~/domain/models/comment/commentRepository'
import { CommentItem } from '~/domain/models/comment/comment'

export class CommentApplicationService {
  constructor(
    private readonly repository: CommentRepository
  ) {}

  public async listProjectComment(projectId: string, options: SearchOption): Promise<CommentListDTO> {
    const item = await this.repository.listAll(projectId, options)
    return new CommentListDTO(item)
  }

  public async list(projectId: string, docId: number): Promise<CommentReadDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map(item => new CommentReadDTO(item))
  }

  public create(projectId: string, docId: number, text: string): Promise<CommentItem> {
    return this.repository.create(projectId, docId, text)
  }

  public update(projectId: string, docId: number, item: CommentReadDTO): Promise<CommentItem> {
    const comment = new CommentItem(
      item.id, item.user, item.username, docId, item.text, item.createdAt
    )
    return this.repository.update(projectId, docId, comment)
  }

  public delete(projectId: string, docId: number, item: CommentReadDTO): Promise<void> {
    return this.repository.delete(projectId, docId, item.id)
  }

  public deleteBulk(projectId: string, items: CommentReadDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.deleteBulk(projectId, ids)
  }
}
