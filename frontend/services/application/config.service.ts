import { ConfigItemList } from '@/models/config/config-item-list'
import { ConfigItemListRepository } from '@/repositories/config/interface'

export class ConfigApplicationService {
  constructor(
    private readonly configRepository: ConfigItemListRepository
  ) {}

  public list(id: string): Promise<ConfigItemList> {
    return this.configRepository.list(id)
  }

  public delete(projectId: string, itemId: number) {
    return this.configRepository.delete(projectId, itemId)
  }
}
