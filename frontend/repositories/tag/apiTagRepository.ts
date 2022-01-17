import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { TagRepository } from '~/domain/models/tag/tagRepository'
import { TagItem } from '~/domain/models/tag/tag'

export class APITagRepository implements TagRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<TagItem[]> {
    const url = `/projects/${projectId}/tags`
    const response = await this.request.get(url)
    return response.data.map((item: any) => plainToInstance(TagItem, item))
  }

  async create(projectId: string, item: string): Promise<TagItem> {
    const url = `/projects/${projectId}/tags`
    const response = await this.request.post(url, { text: item })
    return plainToInstance(TagItem, response.data)
  }

  async delete(projectId: string, tagId: number): Promise<void> {
    const url = `/projects/${projectId}/tags/${tagId}`
    await this.request.delete(url)
  }
}
