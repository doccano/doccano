import { Format } from '~/domain/models/download/format'

export class FormatDTO {
  name: string
  example: string
  properties: object

  constructor(item: Format) {
    this.name = item.name
    this.example = item.example
    this.properties = item.properties
  }
}
