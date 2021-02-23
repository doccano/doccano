import { CommentItem, CommentItemList } from '@/models/comment'
import { CommentItemListRepository } from '@/repositories/comment/interface'

export class CommentApplicationService {
  constructor(
    private readonly repository: CommentItemListRepository
  ) {}

  public listProjectComment(projectId: string, q: string = ''): Promise<CommentItemList> {
    return this.repository.listAll(projectId, q)
  }

  public list(projectId: string, docId: string): Promise<CommentItemList> {
    return this.repository.list(projectId, docId)
  }

  public create(projectId: string, docId: string, text: string): Promise<CommentItem> {
    return this.repository.create(projectId, docId, text)
  }

  public update(projectId: string, docId: string, item: CommentItem): Promise<CommentItem> {
    return this.repository.update(projectId, docId, item)
  }

  public delete(projectId: string, docId: string, item: CommentItem): Promise<void> {
    return this.repository.delete(projectId, docId, item)
  }

  public deleteBulk(projectId: string, items: CommentItemList): Promise<void> {
    return this.repository.deleteBulk(projectId, items)
  }
}
