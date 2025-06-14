import ApiService from '@/services/api.service'
import { LabelRepository } from '@/domain/models/label/labelRepository'
import { LabelItem } from '@/domain/models/label/label'

function toModel(item: { [key: string]: any }): LabelItem {
  return new LabelItem(
    item.id,
    item.text,
    item.prefix_key,
    item.suffix_key,
    item.background_color,
    item.text_color
  )
}

function toPayload(item: LabelItem): { [key: string]: any } {
  return {
    id: item.id,
    text: item.text,
    prefix_key: item.prefixKey,
    suffix_key: item.suffixKey,
    background_color: item.backgroundColor,
    text_color: item.textColor
  }
}

export class APILabelRepository implements LabelRepository {
  constructor(private readonly baseUrl = 'label', private readonly request = ApiService) {}

  async list(projectId: string): Promise<LabelItem[]> {
    const url = `/projects/${projectId}/${this.baseUrl}s`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async findById(projectId: string, labelId: number): Promise<LabelItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s/${labelId}`
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async create(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async update(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s/${item.id}`
    const payload = toPayload(item)
    const response = await this.request.patch(url, payload)
    return toModel(response.data)
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
