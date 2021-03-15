import { TextClassificationItem } from '~/domain/models/tasks/textClassification'

export interface TextClassificationRepository {
  list(projectId: string, docId: number): Promise<TextClassificationItem[]>

  create(projectId: string, docId: number, labelId: number): Promise<void>

  delete(projectId: string, docId: number, annotationId: number): Promise<void>

  clear(projectId: string, docId: number): Promise<void>

  autoLabel(projectId: string, docId: number): Promise<void>
}
