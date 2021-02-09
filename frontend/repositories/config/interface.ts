import { ConfigItem, ConfigItemList } from '@/models/config/config-item-list'

export interface ConfigItemListRepository {
  list(projectId: string): Promise<ConfigItemList>

  create(projectId: string, item: ConfigItem): Promise<ConfigItem>

  delete(projectId: string, itemId: number): Promise<void>

  update(projectId: string, item: ConfigItem): Promise<ConfigItem>
}
