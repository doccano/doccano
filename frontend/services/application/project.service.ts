import { ProjectItem, CurrentUsersRole } from '@/models/project'
import { ProjectItemListRepository } from '@/repositories/project/interface'

export class ProjectDTO {
  id:                          number
  name:                        string
  description:                 string
  guideline:                   string
  users:                       number[]
  current_users_role:          CurrentUsersRole
  project_type:                string
  updated_at:                  string
  randomize_document_order:    boolean
  collaborative_annotation:    boolean
  single_class_classification: boolean
  resourcetype:                string

  constructor(item: ProjectItem) {
    this.id = item.id
    this.name = item.name
    this.description = item.description
    this.guideline = item.guideline
    this.users = item.users
    this.current_users_role = item.current_users_role
    this.project_type = item.project_type
    this.updated_at = item.updated_at
    this.randomize_document_order = item.randomize_document_order
    this.collaborative_annotation = item.collaborative_annotation
    this.single_class_classification = item.single_class_classification
    this.resourcetype = item.resourcetype
  }
}

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

  public async create(item: ProjectDTO): Promise<void> {
    try {
      const project = this.toItem(item)
      await this.repository.create(project)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(item: ProjectDTO): Promise<void> {
    try {
      const project = this.toItem(item)
      await this.repository.update(project)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(items: ProjectDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(ids)
  }

  private toItem(item: ProjectDTO): ProjectItem {
    return new ProjectItem(
      item.id,
      item.name,
      item.description,
      item.guideline,
      item.users,
      item.current_users_role,
      item.project_type,
      item.updated_at,
      item.randomize_document_order,
      item.collaborative_annotation,
      item.single_class_classification,
      item.resourcetype
    )
  }
}
