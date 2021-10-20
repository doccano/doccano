import { LinkTypeDTO } from './linkData';
import { LinkTypesRepository } from '~/domain/models/links/linkTypesRepository';
import { LinkTypeItem } from '~/domain/models/links/link';


export class LinkTypesApplicationService {
  constructor(
    private readonly repository: LinkTypesRepository
  ) {}

  public async list(id: string): Promise<LinkTypeDTO[]> {
    const items = await this.repository.list(id)
    return items.map(item => new LinkTypeDTO(item))
  }

  public create(projectId: string, item: LinkTypeDTO): void {
    const label = new LinkTypeItem(0, item.text, item.color)
    this.repository.create(projectId, label)
  }

  public update(projectId: string, item: LinkTypeDTO): void {
    const label = new LinkTypeItem(item.id, item.text, item.color)
    this.repository.update(projectId, label)
  }

  public bulkDelete(projectId: string, items: LinkTypeDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }
}
