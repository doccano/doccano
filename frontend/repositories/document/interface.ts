import { DocumentItem, DocumentItemList } from '@/models/document'

export type SearchOption = {[key: string]: string | (string | null)[]}

export interface DocumentItemRepository {
  list(projectId: string, { limit, offset, q, isChecked, filterName }: SearchOption): Promise<DocumentItemList>

  create(projectId: string, item: DocumentItem): Promise<DocumentItem>

  update(projectId: string, item: DocumentItem): Promise<DocumentItem>

  bulkDelete(projectId: string, ids: number[]): Promise<void>

  deleteAll(projectId: string): Promise<void>

  uploadFile(projectId: string, payload: FormData): Promise<void>

  exportFile(projectId: string, format: string, onlyApproved: boolean): Promise<any>
}
