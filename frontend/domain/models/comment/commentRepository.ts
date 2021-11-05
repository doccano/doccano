import { CommentItem } from '~/domain/models/comment/comment'

export interface CommentItemResponse {
  id: number,
  user: number,
  username: string,
  example: string,
  text: string,
  created_at: string
}

export interface CommentRepository {
  listAll(projectId: string, q: string): Promise<CommentItem[]>

  list(projectId: string, docId: string): Promise<CommentItem[]>

  create(projectId: string, docId: string, text: string): Promise<CommentItem>

  update(projectId: string, docId: string, item: CommentItem): Promise<CommentItem>

  delete(projectId: string, docId: string, commentId: number): Promise<void>

  deleteBulk(projectId: string, items: number[]): Promise<void>
}
