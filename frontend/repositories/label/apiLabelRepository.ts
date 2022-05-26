import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { LabelRepository } from '~/domain/models/label/labelRepository'
import { LabelItem } from '~/domain/models/label/label'

export interface LabelItemResponse {
  id: number
  text: string
  prefix_key: string
  suffix_key: string
  background_color: string
  text_color: string
}

export class APILabelRepository implements LabelRepository {
  constructor(private readonly baseUrl = 'label', private readonly request = ApiService) {}

  async list(projectId: string): Promise<LabelItem[]> {
    const url = `/projects/${projectId}/${this.baseUrl}s`
    const response = await this.request.get(url)
    return response.data.map((item: any) => plainToInstance(LabelItem, item))
  }

  async findById(projectId: string, labelId: number): Promise<LabelItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s/${labelId}`
    const response = await this.request.get(url)
    return plainToInstance(LabelItem, response.data)
  }

  async create(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s`
    const response = await this.request.post(url, item.toObject())
    return plainToInstance(LabelItem, response.data)
  }

  async update(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    return plainToInstance(LabelItem, response.data)
  }

  async bulkDelete(projectId: string, labelIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/${this.baseUrl}s`
    await this.request.delete(url, { ids: labelIds })
  }

  async uploadFile(projectId: string, payload: FormData): Promise<void> {
    const url = `/projects/${projectId}/${this.baseUrl}-upload`
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    try {
      await this.request.post(url, payload, config)
    } catch (e: any) {
      const data = e.response.data
      if ('detail' in data) {
        throw new Error(data.detail)
      } else {
        throw new Error('Text field is required')
      }
    }
  }
}
