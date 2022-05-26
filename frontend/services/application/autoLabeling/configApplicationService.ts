import { ConfigRepository } from '~/domain/models/autoLabeling/configRepository'
import { ConfigItemList, ConfigItem } from '~/domain/models/autoLabeling/config'

export class ConfigApplicationService {
  constructor(private readonly configRepository: ConfigRepository) {}

  public list(id: string): Promise<ConfigItemList> {
    return this.configRepository.list(id)
  }

  public save(projectId: string, item: ConfigItem): Promise<ConfigItem> {
    return this.configRepository.create(projectId, item)
  }

  public delete(projectId: string, itemId: number) {
    return this.configRepository.delete(projectId, itemId)
  }

  public testParameters(projectId: string, item: ConfigItem, text: string) {
    return this.configRepository
      .testParameters(projectId, item, text)
      .then((value) => {
        return value
      })
      .catch((error) => {
        const data = error.response.data
        throw new Error(data)
      })
  }

  public testTemplate(projectId: string, response: any, item: ConfigItem) {
    return this.configRepository
      .testTemplate(projectId, response, item)
      .then((value) => {
        return value
      })
      .catch((error) => {
        const data = error.response.data
        throw new Error(data)
      })
  }

  public testMapping(projectId: string, item: ConfigItem, response: any) {
    return this.configRepository
      .testMapping(projectId, item, response)
      .then((value) => {
        return value
      })
      .catch((error) => {
        const data = error.response.data
        throw new Error(data)
      })
  }
}
