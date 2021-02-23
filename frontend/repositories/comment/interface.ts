import { CommentItem, CommentItemList } from '@/models/comment'

export interface CommentItemResponse {
  id: number,
  user: number,
  username: string,
  document: number,
  document_text: string,
  text: string,
  created_at: string
}

export interface CommentItemListRepository {
  listAll(projectId: string, q: string): Promise<CommentItemList>

  list(projectId: string, docId: string): Promise<CommentItemList>

  create(projectId: string, docId: string, text: string): Promise<CommentItem>

  update(projectId: string, docId: string, item: CommentItem): Promise<CommentItem>

  delete(projectId: string, docId: string, item: CommentItem): Promise<void>

  deleteBulk(projectId: string, items: CommentItemList): Promise<void>
}
