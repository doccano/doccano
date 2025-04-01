import { PerspectiveDTO } from './perspectiveData'
import { CreatePerspectiveCommand } from './perspectiveCommand'
import { PerspectiveRepository } from '~/domain/models/perspective/perspectiveRepository'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveApplicationService {
  constructor(private readonly repository: PerspectiveRepository) {}

  public async create(projectId: string, item: CreatePerspectiveCommand): Promise<PerspectiveDTO> {
    const perspective = PerspectiveItem.create(item.project_id, item.questions, item.members)
    const created = await this.repository.create(projectId, perspective)
    return new PerspectiveDTO(created)
  }

  public async list(projectId: string): Promise<PerspectiveDTO[]> {
    const perspectives = await this.repository.list(projectId)
    return perspectives.map((perspective) => new PerspectiveDTO(perspective))
  }
}
