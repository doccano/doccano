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
    this.fromId = item.fromId
    this.toId = item.toId
    this.labelId = item.type
  }
}