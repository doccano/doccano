import { LinkItem } from '~/domain/models/links/link'

export class LinkDTO {
  id: number
  text: string
  prefixKey: string | null
  suffixKey: string | null
  backgroundColor: string
  textColor: string

  constructor(item: LinkItem) {
    this.id = item.id
    this.text = item.text
    this.prefixKey = item.prefixKey
    this.suffixKey = item.suffixKey
    this.backgroundColor = item.backgroundColor
    this.textColor = '#ffffff'
  }
}
