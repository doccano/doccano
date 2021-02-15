import { ConfigItemList, ConfigItem } from '@/models/config/config-item-list'
import { ConfigItemListRepository, ConfigTestResponse } from '@/repositories/config/interface'

export class ConfigApplicationService {
  constructor(
    private readonly configRepository: ConfigItemListRepository
  ) {}

  public list(id: string): Promise<ConfigItemList> {
    return this.configRepository.list(id)
  }

  public save(projectId: string, item: ConfigItem): Promise<ConfigItem> {
    return this.configRepository.create(projectId, item)
  }

  public delete(projectId: string, itemId: number) {
    return this.configRepository.delete(projectId, itemId)
  }

  public testConfig(projectId: string, item: ConfigItem, text: string): Promise<ConfigTestResponse> {
    return this.configRepository.testConfig(projectId, item, text)
  }
}
