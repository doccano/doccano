import { Catalog } from '~/domain/models/upload/catalog'


export class CatalogDTO {
  name: string
  example: string
  acceptTypes: string
  properties: object

  constructor(item: Catalog) {
    this.name = item.name
    this.example = item.example
    this.acceptTypes = item.acceptTypes
    this.properties = item.properties
  }
}
