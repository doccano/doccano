import { CatalogDTO } from './catalogData'
import { CatalogRepository } from '~/domain/models/upload/catalogRepository'

export class CatalogApplicationService {
  constructor(private readonly repository: CatalogRepository) {}

  public async list(projectId: string): Promise<CatalogDTO[]> {
    const items = await this.repository.list(projectId)
    return items.map((item) => new CatalogDTO(item))
  }
}
