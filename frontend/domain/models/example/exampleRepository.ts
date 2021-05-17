import { ExampleItem, ExampleItemList } from '~/domain/models/example/example'

export type SearchOption = {[key: string]: string | (string | null)[]}

export interface ExampleRepository {
  list(projectId: string, { limit, offset, q, isChecked, filterName }: SearchOption): Promise<ExampleItemList>

  create(projectId: string, item: ExampleItem): Promise<ExampleItem>

  update(projectId: string, item: ExampleItem): Promise<ExampleItem>

  bulkDelete(projectId: string, ids: number[]): Promise<void>

  deleteAll(projectId: string): Promise<void>

  uploadFile(projectId: string, payload: FormData): Promise<void>

  exportFile(projectId: string, format: string, onlyApproved: boolean): Promise<any>

  approve(projectId: string, docId: number, approved: boolean): Promise<void>
}
