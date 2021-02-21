import ApiService from '@/services/api.service'
import { LabelItemListRepository } from '@/repositories/label/interface'
import { LabelItemList, LabelItem } from '@/models/label'

export interface LabelItemResponse {
  id: number,
  text: string,
  prefix_key: string,
  suffix_key: string,
  background_color: string,
  text_color: string
}

export class FromApiLabelItemListRepository implements LabelItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<LabelItemList> {
    const url = `/projects/${projectId}/labels`
    const response = await this.request.get(url)
    const responseItems: LabelItemResponse[] = response.data
    return LabelItemList.valueOf(
      responseItems.map(item => LabelItem.valueOf(item))
    )
  }

  async create(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/labels`
    const response = await this.request.post(url, item.toObject())
    const responseItem: LabelItemResponse = response.data
    return LabelItem.valueOf(responseItem)
  }

  async update(projectId: string, item: LabelItem): Promise<LabelItem> {
    const url = `/projects/${projectId}/labels/${item.id}`
    const response = await this.request.put(url, item.toObject())
    const responseItem: LabelItemResponse = response.data
    return LabelItem.valueOf(responseItem)
  }

  async delete(projectId: string, itemId: number): Promise<void> {
    const url = `/projects/${projectId}/labels/${itemId}`
    await this.request.delete(url)
  }
}
