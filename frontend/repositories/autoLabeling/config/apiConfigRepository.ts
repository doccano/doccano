import ApiService from '@/services/api.service'
import { ConfigRepository, ConfigTestResponse } from '~/domain/models/autoLabeling/configRepository'
import { ConfigItemList, ConfigItem } from '~/domain/models/autoLabeling/config'

export interface ConfigItemResponse {
  id: number,
  model_name: string,
  model_attrs: object,
  template: string,
  label_mapping: object
}

export class APIConfigRepository implements ConfigRepository {
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

  async testConfig(projectId: string, item: ConfigItem, text: string): Promise<ConfigTestResponse> {
    const url = `/projects/${projectId}/auto-labeling-config-testing`
    const response = await this.request.post(url, {config: {...item.toAPI()}, input: text})
    const responseItem: ConfigTestResponse = response.data
    return responseItem
  }

  async testParameters(item: ConfigItem, text: string) {
    const url = 'auto-labeling-parameter-testing'
    const response = await this.request.post(url, {...item.toAPI(), text})
    const responseItem: ConfigTestResponse = response.data
    return responseItem
  }

  async testTemplate(projectId: string, response: any, item: ConfigItem): Promise<ConfigTestResponse> {
    console.log(projectId)
    const url = `/projects/${projectId}/auto-labeling-template-testing`
    const _response = await this.request.post(url, { response, ...item.toAPI() })
    const responseItem: ConfigTestResponse = _response.data
    return responseItem
  }

  async testMapping(projectId: string, item: ConfigItem, response: any): Promise<ConfigTestResponse> {
    const url = `/projects/${projectId}/auto-labeling-mapping-testing`
    const _response = await this.request.post(url, {...item.toAPI(), response})
    const responseItem: ConfigTestResponse = _response.data
    return responseItem
  }
}
