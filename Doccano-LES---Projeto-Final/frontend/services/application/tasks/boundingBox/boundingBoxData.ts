import { BoundingBox } from '@/domain/models/tasks/boundingBox'

export class BoundingBoxDTO {
  id: number
  uuid: string
  label: number
  x: number
  y: number
  width: number
  height: number

  constructor(item: BoundingBox) {
    this.id = item.id
    this.uuid = item.uuid
    this.label = item.label
    this.x = item.x
    this.y = item.y
    this.width = item.width
    this.height = item.height
  }
}
