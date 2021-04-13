import { TagItem } from '~/domain/models/tag/tag'

export class TagDTO {
  id: number
  text: string
  project: string

  constructor(item: TagItem) {
    this.id = item.id
    this.text = item.text
    this.project = item.project
  }
}
