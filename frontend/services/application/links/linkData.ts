import { LinkTypeItem, LinkItem } from '~/domain/models/links/link'

export class LinkTypeDTO {
  id: number
  name: string
  color: string

  constructor(item: LinkTypeItem) {
    this.id = item.id
    this.name = item.name
    this.color = item.color
  }
}

export class LinkDTO {
  id: number
  annotation_id_1: number
  annotation_id_2: number
  type: number

  constructor(item: LinkItem) {
    this.id = item.id
    this.annotation_id_1 = item.annotation_id_1
    this.annotation_id_2 = item.annotation_id_2
    this.type = item.type
  }
}