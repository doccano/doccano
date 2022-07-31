import { Relation } from '@/domain/models/tasks/relation'

export class RelationDTO {
  id: number
  fromId: number
  toId: number
  labelId: number

  constructor(item: Relation) {
    this.id = item.id
    this.fromId = item.fromId
    this.toId = item.toId
    this.labelId = item.type
  }
}
