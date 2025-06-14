import { PerspectiveDTO } from './perspectiveData'
import { CreatePerspectiveCommand } from './perspectiveCommand'
import { PerspectiveRepository } from '~/domain/models/perspective/perspectiveRepository'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveApplicationService {
  constructor(private readonly repository: PerspectiveRepository) {}

  public async create(projectId: string, item: CreatePerspectiveCommand): Promise<PerspectiveDTO> {
    const perspective = PerspectiveItem.create(
      item.name,
      item.project_id,
      item.questions.map(q => ({ ...q, perspective_id: q.perspective_id ?? 0 })),
      item.members
    )
    const created = await this.repository.create(projectId, perspective)
    return new PerspectiveDTO(created)
  }

  public async list(projectId: string): Promise<PerspectiveDTO[]> {
    const perspectives = await this.repository.list(projectId)
    return perspectives.map(p => new PerspectiveDTO(p))
  }
}
