import { CommentItem, CommentItemList } from '~/domain/models/comment/comment'

export interface CommentItemResponse {
  id: number,
  user: number,
  username: string,
  example: number,
  text: string,
  created_at: string
}

export type SearchOption = {[key: string]: string | (string | null)[]}

export interface CommentRepository {
  listAll(projectId: string, { limit, offset, q }: SearchOption): Promise<CommentItemList>

  list(projectId: string, docId: number): Promise<CommentItem[]>

  create(projectId: string, docId: number, text: string): Promise<CommentItem>

  update(projectId: string, docId: number, item: CommentItem): Promise<CommentItem>

  delete(projectId: string, docId: number, commentId: number): Promise<void>

  deleteBulk(projectId: string, items: number[]): Promise<void>
}
