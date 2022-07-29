import ApiService from '@/services/api.service'
import { TagRepository } from '@/domain/models/tag/tagRepository'
import { TagItem } from '@/domain/models/tag/tag'

function toModel(item: { [key: string]: any }): TagItem {
  return new TagItem(item.id, item.text, item.project)
}

export class APITagRepository implements TagRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: string): Promise<TagItem[]> {
    const url = `/projects/${projectId}/tags`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, text: string): Promise<TagItem> {
    const url = `/projects/${projectId}/tags`
    const response = await this.request.post(url, { text })
    return toModel(response.data)
  }

  async delete(projectId: string, tagId: number): Promise<void> {
    const url = `/projects/${projectId}/tags/${tagId}`
    await this.request.delete(url)
  }
}
