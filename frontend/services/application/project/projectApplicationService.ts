import { ProjectDTO, ProjectWriteDTO, ProjectListDTO, SearchQueryData } from './projectData'
import { ProjectRepository, SearchQuery } from '~/domain/models/project/projectRepository'
import { ProjectWriteItem } from '~/domain/models/project/project'

export class ProjectApplicationService {
  constructor(private readonly repository: ProjectRepository) {}

  public async list(q: SearchQueryData): Promise<ProjectListDTO> {
    try {
      const query = new SearchQuery(q.limit, q.offset, q.q, q.sortBy, q.sortDesc)
      const items = await this.repository.list(query)
      return new ProjectListDTO(items)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async findById(id: string): Promise<ProjectDTO> {
    const item = await this.repository.findById(id)
    return new ProjectDTO(item)
  }

  public async create(item: ProjectWriteDTO): Promise<ProjectDTO> {
    try {
      const project = this.toWriteModel(item)
      const response = await this.repository.create(project)
      return new ProjectDTO(response)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(item: ProjectWriteDTO): Promise<void> {
    try {
      const project = this.toWriteModel(item)
      project.tags = []
      await this.repository.update(project)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(items: ProjectDTO[]): Promise<void> {
    const ids = items.map((item) => item.id)
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
      item.graphemeMode,
      item.useRelation,
      item.tags
    )
  }
}
