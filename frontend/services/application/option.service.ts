import { OptionItem } from '@/models/option'
import { OptionRepository } from '@/repositories/option/interface'

export class OptionDTO {
  page: number
  q?: string
  isChecked?: string

  constructor(item: OptionItem) {
    this.page = item.page
    this.q = item.q
    this.isChecked = item.isChecked
  }
}

export class OptionApplicationService {
  constructor(
    private readonly repository: OptionRepository
  ) {}

  public findOption(projectId: string): OptionDTO {
    const item = this.repository.findById(projectId)
    return new OptionDTO(item)
  }

  public save(projectId: string, option: OptionDTO) {
    const item = new OptionItem(option.page, option.q, option.isChecked)
    this.repository.save(projectId, item)
  }
}
