import { TagRepository } from '~/domain/models/tag/tagRepository'

export class TagApplicationService {
  constructor(private readonly repository: TagRepository) {}

  public async bulkUpdate(projectId: string | number, tags: string[]): Promise<void> {
    const currentTags = await this.repository.list(projectId)
    const currentTagNames = currentTags.map((tag) => tag.text)
    const addedTagNames = tags.filter((tag) => !currentTagNames.includes(tag))
    const deletedTagIds = currentTags.filter((tag) => !tags.includes(tag.text)).map((tag) => tag.id)
    await Promise.all(addedTagNames.map((tag) => this.repository.create(projectId, tag)))
    await Promise.all(deletedTagIds.map((id) => this.repository.delete(projectId, id)))
  }
}
