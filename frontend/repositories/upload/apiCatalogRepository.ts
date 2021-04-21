import ApiService from '@/services/api.service'
import { CatalogRepository } from '@/domain/models/upload/catalogRepository'
import { Catalog } from '~/domain/models/upload/catalog'

export class APICatalogRepository implements CatalogRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<Catalog[]> {
    const url = `/projects/${projectId}/catalog`
    const response = await this.request.get(url)
    const responseItems: Catalog[] = response.data
    return responseItems.map(item => Catalog.valueOf(item))
  }
}
