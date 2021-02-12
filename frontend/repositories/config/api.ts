import ApiService from '@/services/api.service'
import { ConfigItemListRepository } from '@/repositories/config/interface'
import { ConfigItemList, ConfigItem } from '@/models/config/config-item-list'

export interface ConfigItemResponse {
  id: number,
  model_name: string,
  model_attrs: object,
  template: string,
  label_mapping: object
}

export class FromApiConfigItemListRepository implements ConfigItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<ConfigItemList> {
    const url = `/projects/${projectId}/auto-labeling-configs`
    const response = await this.request.get(url)
    const responseItems: ConfigItemResponse[] = response.data
    return ConfigItemList.valueOf(
      responseItems.map(item => ConfigItem.valueOf(item))
    )
  }

  async create(projectId: string, item: ConfigItem): Promise<ConfigItem> {
    const url = `/projects/${projectId}/auto-labeling-configs`
    const response = await this.request.post(url, {
      model_name: item.modelName,
      model_attrs: item.modelAttrs,
      template: item.template,
      label_mapping: item.labelMapping
    })
    const responseItem: ConfigItemResponse = response.data
    return ConfigItem.valueOf(responseItem)
  }

  async update(projectId: string, item: ConfigItem): Promise<ConfigItem> {
    const url = `/projects/${projectId}/auto-labeling-configs/${item.id}`
    const response = await this.request.put(url, {
      id: item.id,
      model_name: item.modelName,
      model_attrs: item.modelAttrs,
      template: item.template,
      label_mapping: item.labelMapping
    })
    const responseItem: ConfigItemResponse = response.data
    return ConfigItem.valueOf(responseItem)
  }

  async delete(projectId: string, itemId: number): Promise<void> {
    const url = `/projects/${projectId}/auto-labeling-configs/${itemId}`
    await this.request.delete(url)
  }
}
