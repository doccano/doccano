import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { Segment } from '@/domain/models/tasks/segmentation'

export class APISegmentationRepository extends AnnotationRepository<Segment> {
  labelName = 'segments'

  toModel(item: { [key: string]: any }): Segment {
    return new Segment(item.id, item.uuid, item.label, item.points)
  }

  toPayload(item: Segment): { [key: string]: any } {
    return {
      id: item.id,
      uuid: item.uuid,
      label: item.label,
      points: item.points
    }
  }
}
