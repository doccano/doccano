import { OptionDTO } from './optionData'
import { OptionRepository } from '~/domain/models/option/optionRepository'
import { OptionItem } from '~/domain/models/option/option'

export class OptionApplicationService {
  constructor(private readonly repository: OptionRepository) {}

  public findOption(projectId: string): OptionDTO {
    const item = this.repository.findById(projectId)
    return new OptionDTO(item)
  }

  public save(projectId: string, option: OptionDTO) {
    const item = new OptionItem(option.page, option.q, option.isChecked)
    this.repository.save(projectId, item)
  }
}
