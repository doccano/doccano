import { LinkTypeItem, LinkItem } from '~/domain/models/links/link'

export class LinkTypeDTO {
  id: number
  text: string
  color: string

  constructor(item: LinkTypeItem) {
    this.id = item.id
    this.text = item.name
    this.color = item.color
  }
}

export class LinkDTO {
  id: number
  fromId: number
  toId: number
  labelId: number

  constructor(item: LinkItem) {
    this.id = item.id
    this.fromId = item.annotation_id_1
    this.toId = item.annotation_id_2
    this.labelId = item.type
  }
}