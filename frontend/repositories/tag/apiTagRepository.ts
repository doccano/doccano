import ApiService from '@/services/api.service'
import { TagRepository } from '~/domain/models/tag/tagRepository'
import { TagItem } from '~/domain/models/tag/tag'

export interface TagItemResponse {
  id: number,
  text: string,
  project: string
}

export class APITagRepository implements TagRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<TagItem[]> {
    const url = `/projects/${projectId}/tags`
    const response = await this.request.get(url)
    const responseItems: TagItemResponse[] = response.data
    return responseItems.map(item => TagItem.valueOf(item))
  }

  async create(projectId: string, item: string): Promise<TagItem> {
    const url = `/projects/${projectId}/tags`
    const response = await this.request.post(url, { text: item })
    const responseItem: TagItemResponse = response.data
    return TagItem.valueOf(responseItem)
  }

  async delete(projectId: string, tagId: number): Promise<void> {
    const url = `/projects/${projectId}/tags/${tagId}`
    await this.request.delete(url)
  }
}
