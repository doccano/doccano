import { LinkDTO } from './linkData';
import { LinksRepository } from '~/domain/models/links/linksRepository';
import { LinkItem } from '~/domain/models/links/link';


export class LinksApplicationService {
  constructor(
    private readonly repository: LinksRepository
  ) {}

  public async list(id: string): Promise<LinkDTO[]> {
    const items = await this.repository.list(id)
    return items.map(item => new LinkDTO(item))
  }

  public create(projectId: string, item: LinkDTO): void {
    const label = new LinkItem(0, item.text, item.prefixKey, item.suffixKey, item.backgroundColor, item.textColor)
    this.repository.create(projectId, label)
  }

  public update(projectId: string, item: LinkDTO): void {
    const label = new LinkItem(item.id, item.text, item.prefixKey, item.suffixKey, item.backgroundColor, item.textColor)
    this.repository.update(projectId, label)
  }

  public bulkDelete(projectId: string, items: LinkDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }
}
