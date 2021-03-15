import { OptionItem } from '~/domain/models/option/option'

export interface OptionRepository {
  findById(projectId: string): OptionItem

  save(projectId: string, option: OptionItem): void
}
