import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { CategoryItem } from '~/domain/models/tasks/textClassification'

export class APITextClassificationRepository extends AnnotationRepository<CategoryItem> {
  constructor() {
    super(CategoryItem)
  }

  protected baseUrl(projectId: string, docId: number): string {
    return `/projects/${projectId}/examples/${docId}/categories`
  }
}
