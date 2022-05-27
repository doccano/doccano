import { plainToInstance } from 'class-transformer'
import { CommentReadDTO, CommentListDTO } from './commentData'
import { CommentRepository, SearchOption } from '~/domain/models/comment/commentRepository'
import { CommentItem } from '~/domain/models/comment/comment'

export class CommentApplicationService {
  constructor(private readonly repository: CommentRepository) {}

  public async listProjectComment(
    projectId: string,
    options: SearchOption
  ): Promise<CommentListDTO> {
    const item = await this.repository.listAll(projectId, options)
    return new CommentListDTO(item)
  }

  public async list(projectId: string, docId: number): Promise<CommentReadDTO[]> {
    const items = await this.repository.list(projectId, docId)
    return items.map((item) => new CommentReadDTO(item))
  }

  public create(projectId: string, docId: number, text: string): Promise<CommentItem> {
    return this.repository.create(projectId, docId, text)
  }

  public update(projectId: string, item: CommentReadDTO): Promise<CommentItem> {
    const comment = plainToInstance(CommentItem, item)
    return this.repository.update(projectId, comment)
  }

  public delete(projectId: string, item: CommentReadDTO): Promise<void> {
    return this.repository.delete(projectId, item.id)
  }

  public deleteBulk(projectId: string, items: CommentReadDTO[]): Promise<void> {
    const ids = items.map((item) => item.id)
    return this.repository.deleteBulk(projectId, ids)
  }
}
