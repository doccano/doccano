import { Catalog } from './catalog'

export interface CatalogRepository {
  list(projectId: string): Promise<Catalog[]>
}
