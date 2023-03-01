import { Page } from '@/domain/models/page'
import { CommentItem } from '~/domain/models/comment/comment'

export type SearchOption = { [key: string]: string | (string | null)[] }

export interface CommentRepository {
  listAll(projectId: string, { limit, offset, q }: SearchOption): Promise<Page<CommentItem>>

  list(projectId: string, docId: number): Promise<CommentItem[]>

  create(projectId: string, docId: number, text: string): Promise<CommentItem>

  update(projectId: string, item: CommentItem): Promise<CommentItem>

  delete(projectId: string, commentId: number): Promise<void>

  deleteBulk(projectId: string, items: number[]): Promise<void>
}
