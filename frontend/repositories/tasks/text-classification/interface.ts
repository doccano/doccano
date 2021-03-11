import { TextClassificationItem } from '@/models/tasks/text-classification'

export interface TextClassificationRepository {
  list(projectId: string, docId: number): Promise<TextClassificationItem[]>

  create(projectId: string, docId: number, labelId: number): Promise<void>

  delete(projectId: string, docId: number, annotationId: number): Promise<void>

  clear(projectId: string, docId: number): Promise<void>
}
