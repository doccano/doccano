import { LabelItem, LabelItemList } from '@/models/label'

export interface LabelItemListRepository {
  list(projectId: string): Promise<LabelItem[]>

  create(projectId: string, item: LabelItem): Promise<LabelItem>

  delete(projectId: string, itemId: number): Promise<void>

  update(projectId: string, item: LabelItem): Promise<LabelItem>

  bulkDelete(projectId: string, labelIds: number[]): Promise<void>

  uploadFile(projectId: string, payload: FormData): Promise<void> 
}
