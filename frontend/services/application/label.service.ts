import { LabelItemList } from '@/models/label'
import { LabelItemListRepository } from '@/repositories/label/interface'

export class LabelApplicationService {
  constructor(
    private readonly repository: LabelItemListRepository
  ) {}

  public list(id: string): Promise<LabelItemList> {
    return this.repository.list(id)
  }
}
