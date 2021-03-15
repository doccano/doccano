import ApiService from '@/services/api.service'
import { LabelRepository } from '~/domain/models/label/labelRepository'
import { LabelItem } from '~/domain/models/label/label'

export interface LabelItemResponse {
  id: number,
  text: string,
  prefix_key: string,
  suffix_key: string,
  background_color: string,
  text_color: string
}

export class APILabelRepository implements LabelRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<LabelItem[]> {
    const url = `/projects/${projectId}/labels`
    const response = await this.request.get(url)
    const responseItems: LabelItemResponse[] = response.data
    return responseItems.map(item => LabelItem.valueOf(item))
  }

  async create(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/labels`
    const response = await this.request.post(url, item.toObject())
    const responseItem: LabelItemResponse = response.data
    return LabelItem.valueOf(responseItem)
  }

  async update(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/labels/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    const responseItem: LabelItemResponse = response.data
    return LabelItem.valueOf(responseItem)
  }

  async bulkDelete(projectId: string, labelIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/labels`
    await this.request.delete(url, { ids: labelIds })
  }

  async uploadFile(projectId: string, payload: FormData): Promise<void> {
    const url = `/projects/${projectId}/label-upload`
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    try {
      await this.request.post(`/projects/${projectId}/label-upload`, payload, config)
    } catch(e) {
      const data = e.response.data
      if ('detail' in data) {
        throw new Error(data.detail)
      } else {
        throw new Error('Text field is required')
      }
    }
  }
}
