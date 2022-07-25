import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { BoundingBoxItem } from '~/domain/models/tasks/boundingBox'

export class ApiBoundingBoxRepository extends AnnotationRepository<BoundingBoxItem> {
  constructor() {
    super(BoundingBoxItem)
  }

  async list(projectId: string, exampleId: number): Promise<BoundingBoxItem[]> {
    const url = `/projects/${projectId}/examples/${exampleId}/bboxes`
    const response = await this.request.get(url)
    return response.data.map((box: any) => BoundingBoxItem.valueOf(box))
  }

  async create(projectId: string, exampleId: number, item: BoundingBoxItem): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/bboxes`
    await this.request.post(url, item.toObject())
  }

  async update(
    projectId: string,
    exampleId: number,
    boxId: number,
    item: BoundingBoxItem
  ): Promise<BoundingBoxItem> {
    const url = `/projects/${projectId}/examples/${exampleId}/bboxes/${boxId}`
    const response = await this.request.patch(url, item.toObject())
    return BoundingBoxItem.valueOf(response.data)
  }

  async delete(projectId: string, exampleId: number, boxId: number): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/bboxes/${boxId}`
    await this.request.delete(url)
  }

  async bulkDelete(projectId: string, exampleId: number, boxIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/bboxes`
    await this.request.delete(url, { ids: boxIds })
  }
}
