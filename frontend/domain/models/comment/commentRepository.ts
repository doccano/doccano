import { CommentItem } from '~/domain/models/comment/comment'

export interface CommentItemResponse {
  id: number,
  user: number,
  username: string,
  document: number,
  document_text: string,
  text: string,
  created_at: string
}

export interface CommentRepository {
  listAll(projectId: string, q: string): Promise<CommentItem[]>

  list(projectId: string, docId: number): Promise<CommentItem[]>

  create(projectId: string, docId: number, text: string): Promise<CommentItem>

  update(projectId: string, docId: number, item: CommentItem): Promise<CommentItem>

  delete(projectId: string, docId: number, commentId: number): Promise<void>

  deleteBulk(projectId: string, items: number[]): Promise<void>
}
