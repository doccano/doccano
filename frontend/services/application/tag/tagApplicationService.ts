import { TagDTO } from './tagData'
import { TagRepository } from '~/domain/models/tag/tagRepository'

export class TagApplicationService {
  constructor(private readonly repository: TagRepository) {}

  public async list(id: string): Promise<TagDTO[]> {
    const items = await this.repository.list(id)
    return items.map((item) => new TagDTO(item))
  }

  public async create(projectId: string, text: string): Promise<void> {
    await this.repository.create(projectId, text)
  }

  public async delete(projectId: string, id: number): Promise<void> {
    return await this.repository.delete(projectId, id)
  }
}
