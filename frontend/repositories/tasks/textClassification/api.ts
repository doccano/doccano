import { AnnotationRepository } from '../interface'
import { TextClassificationItem } from '~/models/tasks/textClassification'


export class FromApiTextClassificationRepository extends AnnotationRepository<TextClassificationItem> {
  constructor() {
    super(TextClassificationItem)
  }

  protected baseUrl(projectId: string, docId: number): string {
    return `/projects/${projectId}/docs/${docId}/annotations`
  }
}
