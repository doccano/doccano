import { ProjectDTO, ProjectWriteDTO } from './projectData'
import { ProjectRepository } from '~/domain/models/project/projectRepository'
import { ProjectWriteItem } from '~/domain/models/project/project'


export class ProjectApplicationService {
  constructor(
    private readonly repository: ProjectRepository
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
      item.enableRandomOrder,
      item.enableShareAnnotation,
      item.singleClassClassification,
      item.allowOverlapping,
      item.graphemeMode
    )
  }
}
