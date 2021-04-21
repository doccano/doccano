import { LabelItem } from '~/domain/models/label/label'

export interface LabelRepository {
  list(projectId: string): Promise<LabelItem[]>

  create(projectId: string, item: LabelItem): Promise<LabelItem>

  update(projectId: string, item: LabelItem): Promise<LabelItem>

  bulkDelete(projectId: string, labelIds: number[]): Promise<void>

  uploadFile(projectId: string, payload: FormData): Promise<void> 
}
