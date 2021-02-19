import { LabelItem, LabelItemList } from '@/models/label'

export interface LabelItemListRepository {
  list(projectId: string): Promise<LabelItemList>

  create(projectId: string, item: LabelItem): Promise<LabelItem>

  delete(projectId: string, itemId: number): Promise<void>

  update(projectId: string, item: LabelItem): Promise<LabelItem>
}
