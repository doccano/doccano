import { OptionItem } from '@/models/option'

export interface OptionRepository {
  findById(projectId: string): OptionItem

  save(projectId: string, option: OptionItem): void
}
