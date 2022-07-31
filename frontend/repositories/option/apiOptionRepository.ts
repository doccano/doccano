import { OptionRepository } from '@/domain/models/option/optionRepository'
import { OptionItem } from '@/domain/models/option/option'

function toPayload(item: OptionItem): { [key: string]: any } {
  return {
    page: item.page,
    q: item.q,
    isChecked: item.isChecked
  }
}

export class LocalStorageOptionRepository implements OptionRepository {
  findById(projectId: string): OptionItem {
    const checkpoint = this.loadCheckpoint()
    if (checkpoint[projectId]) {
      const option = checkpoint[projectId]
      return new OptionItem(option.page, option.q, option.isChecked)
    } else {
      return new OptionItem(1)
    }
  }

  save(projectId: string, option: OptionItem): void {
    const checkpoint = this.loadCheckpoint()
    checkpoint[projectId] = toPayload(option)
    localStorage.setItem('checkpoint', JSON.stringify(checkpoint))
  }

  loadCheckpoint(): { [key: string]: any } {
    const item = localStorage.getItem('checkpoint') || '{}'
    return JSON.parse(item)
  }
}
