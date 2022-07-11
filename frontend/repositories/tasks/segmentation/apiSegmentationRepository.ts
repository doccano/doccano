import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { SegmentationItem } from '~/domain/models/tasks/segmentation'

export class ApiSegmentationRepository extends AnnotationRepository<SegmentationItem> {
  constructor() {
    super(SegmentationItem)
  }

  async list(projectId: string, exampleId: number): Promise<SegmentationItem[]> {
    const url = `/projects/${projectId}/examples/${exampleId}/segments`
    const response = await this.request.get(url)
    return response.data.map((box: any) => SegmentationItem.valueOf(box))
  }

  async create(projectId: string, exampleId: number, item: SegmentationItem): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/segments`
    await this.request.post(url, item.toObject())
  }

  async update(
    projectId: string,
    exampleId: number,
    boxId: number,
    item: SegmentationItem
  ): Promise<SegmentationItem> {
    const url = `/projects/${projectId}/examples/${exampleId}/segments/${boxId}`
    const response = await this.request.patch(url, item.toObject())
    return SegmentationItem.valueOf(response.data)
  }

  async delete(projectId: string, exampleId: number, boxId: number): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/segments/${boxId}`
    await this.request.delete(url)
  }

  async bulkDelete(projectId: string, exampleId: number, boxIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/segments`
    await this.request.delete(url, { ids: boxIds })
  }
}
