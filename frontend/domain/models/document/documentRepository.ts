import { DocumentItem, DocumentItemList } from '~/domain/models/document/document'

export type SearchOption = {[key: string]: string | (string | null)[]}

export interface DocumentRepository {
  list(projectId: string, { limit, offset, q, isChecked, filterName }: SearchOption): Promise<DocumentItemList>

  create(projectId: string, item: DocumentItem): Promise<DocumentItem>

  update(projectId: string, item: DocumentItem): Promise<DocumentItem>

  bulkDelete(projectId: string, ids: number[]): Promise<void>

  deleteAll(projectId: string): Promise<void>

  uploadFile(projectId: string, payload: FormData): Promise<void>

  exportFile(projectId: string, format: string, onlyApproved: boolean): Promise<any>

  approve(projectId: string, docId: number, approved: boolean): Promise<void>
}
