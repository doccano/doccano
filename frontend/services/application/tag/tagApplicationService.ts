import { TagDTO } from './tagData'
import { TagRepository } from '~/domain/models/tag/tagRepository'
import { TagItem } from '~/domain/models/tag/tag'


export class TagApplicationService {
  constructor(
    private readonly repository: TagRepository
  ) {}

  public async list(id: string): Promise<TagDTO[]> {
    const items = await this.repository.list(id)
    return items.map(item => new TagDTO(item))
  }

  public create(projectId: string, text: string): void {
    this.repository.create(projectId, text)
  }

  public delete(projectId: string, id: number): Promise<void> {
    return this.repository.delete(projectId, id)
  }
}
