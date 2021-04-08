import { Catalog } from '~/domain/models/upload/catalog'


export class CatalogDTO {
  name: string
  properties: object

  constructor(item: Catalog) {
    this.name = item.name
    this.properties = item.properties
  }
}
