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

  public async bulkUpdate(projectId: string | number, tags: string[]): Promise<void> {
    const currentTags = await this.repository.list(projectId)
    const currentTagNames = currentTags.map((tag) => tag.text)
    const addedTagNames = tags.filter((tag) => !currentTagNames.includes(tag))
    const deletedTagIds = currentTags.filter((tag) => !tags.includes(tag.text)).map((tag) => tag.id)
    await Promise.all(addedTagNames.map((tag) => this.repository.create(projectId, tag)))
    await Promise.all(deletedTagIds.map((id) => this.repository.delete(projectId, id)))
  }
}
