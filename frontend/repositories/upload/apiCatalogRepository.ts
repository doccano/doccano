import { plainToInstance } from 'class-transformer'
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
    return response.data.map((item: any) => plainToInstance(Catalog, item))
  }
}
