import { ProjectReadItem, ProjectWriteItem, CurrentUsersRole, ProjectType } from '@/models/project'
import { ProjectItemListRepository } from '@/repositories/project/interface'

export class ProjectDTO {
  id:                          number
  name:                        string
  description:                 string
  guideline:                   string
  current_users_role:          CurrentUsersRole
  projectType:                 ProjectType
  updatedAt:                   string
  enableRandomizeDocOrder:     boolean
  enableShareAnnotation:       boolean

  constructor(item: ProjectReadItem) {
    this.id = item.id
    this.name = item.name
    this.description = item.description
    this.guideline = item.guideline
    this.current_users_role = item.current_users_role
    this.projectType = item.project_type
    this.updatedAt = item.updated_at
    this.enableRandomizeDocOrder = item.randomize_document_order
    this.enableShareAnnotation = item.collaborative_annotation
  }
}

export type ProjectWriteDTO = Pick<ProjectDTO, 'id' | 'name' | 'description' | 'guideline' | 'projectType' | 'enableRandomizeDocOrder' | 'enableShareAnnotation'>

export class ProjectApplicationService {
  constructor(
    private readonly repository: ProjectItemListRepository
  ) {}

  public async list(): Promise<ProjectDTO[]> {
    try {
      const items = await this.repository.list()
      return items.map(item => new ProjectDTO(item))
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async findById(id: string): Promise<ProjectDTO> {
    const item = await this.repository.findById(id)
    const response = new ProjectDTO(item)
    return new ProjectDTO(item)
  }

  public async create(item: ProjectWriteDTO): Promise<ProjectDTO> {
    try {
      const project = this.toWriteModel(item)
      const response = await this.repository.create(project)
      return new ProjectDTO(response)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(item: ProjectWriteDTO): Promise<void> {
    try {
      const project = this.toWriteModel(item)
      await this.repository.update(project)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(items: ProjectDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(ids)
  }

  private toWriteModel(item: ProjectWriteDTO): ProjectWriteItem {
    return new ProjectWriteItem(
      item.id,
      item.name,
      item.description,
      item.guideline,
      item.projectType,
      item.enableRandomizeDocOrder,
      item.enableShareAnnotation
    )
  }
}
