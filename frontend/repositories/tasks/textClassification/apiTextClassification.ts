import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { TextClassificationItem } from '~/domain/models/tasks/textClassification'


export class APITextClassificationRepository extends AnnotationRepository<TextClassificationItem> {
  constructor() {
    super(TextClassificationItem)
  }

  protected baseUrl(projectId: string, docId: number): string {
    return `/projects/${projectId}/examples/${docId}/categories`
  }
}
