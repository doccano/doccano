import { AnnotationApplicationService } from '../annotationApplicationService'
import { SegmentationDTO } from './segmentationData'
import { Segment } from '@/domain/models/tasks/segmentation'

export class SegmentationApplicationService extends AnnotationApplicationService<Segment> {
  public async list(projectId: string, exampleId: number): Promise<SegmentationDTO[]> {
    const items = await this.repository.list(projectId, exampleId)
    return items.map((item) => new SegmentationDTO(item))
  }

  public async create(
    projectId: string,
    exampleId: number,
    uuid: string,
    label: number,
    points: number[]
  ): Promise<void> {
    const item = new Segment(0, uuid, label, points)
    try {
      await this.repository.create(projectId, exampleId, item)
    } catch (e: any) {
      console.log(e.response.data.detail)
    }
  }

  public async update(
    projectId: string,
    exampleId: number,
    annotationId: number,
    item: SegmentationDTO
  ): Promise<void> {
    const bbox = new Segment(item.id, item.uuid, item.label, item.points)
    try {
      await this.repository.update(projectId, exampleId, annotationId, bbox)
    } catch (e: any) {
      console.log(e.response.data.detail)
    }
  }
}
