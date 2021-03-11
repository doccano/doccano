import { OptionItem } from '@/models/option'
import { OptionRepository } from './interface'

export class LocalStorageOptionRepository implements OptionRepository {

  findById(projectId: string): OptionItem {
    const checkpoint = this.loadCheckpoint()
    return OptionItem.valueOf(checkpoint[projectId] ? checkpoint[projectId] : { page: 1 })
  }

  save(projectId: string, option: OptionItem): void {
    const checkpoint = this.loadCheckpoint()
    checkpoint[projectId] = option.toObject()
    localStorage.setItem('checkpoint', JSON.stringify(checkpoint))
  }

  loadCheckpoint() {
    const item = localStorage.getItem('checkpoint') || '{}'
    return JSON.parse(item)
  }
}
