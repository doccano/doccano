import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { Span } from '@/domain/models/tasks/span'

export class APISpanRepository extends AnnotationRepository<Span> {
  labelName = 'spans'

  toModel(item: { [key: string]: any }): Span {
    return new Span(item.id, item.label, item.user, item.start_offset, item.end_offset)
  }

  toPayload(item: Span): { [key: string]: any } {
    return {
      id: item.id,
      label: item.label,
      user: item.user,
      start_offset: item.startOffset,
      end_offset: item.endOffset
    }
  }
}
