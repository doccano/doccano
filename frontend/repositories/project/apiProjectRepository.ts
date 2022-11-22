import { Page } from '@/domain/models/page'
import { Project } from '@/domain/models/project/project'
import { ProjectRepository, SearchQuery } from '@/domain/models/project/projectRepository'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): Project {
  return new Project(
    item.id,
    item.name,
    item.description,
    item.guideline,
    item.project_type,
    item.random_order,
    item.collaborative_annotation,
    item.single_class_classification,
    item.allow_overlapping,
    item.grapheme_mode,
    item.use_relation,
    item.tags,
    item.users,
    item.created_at,
    item.updated_at,
    item.author,
    item.is_text_project
  )
}

function toPayload(item: Project): { [key: string]: any } {
  return {
    id: item.id,
    name: item.name,
    description: item.description,
    guideline: item.guideline,
    project_type: item.projectType,
    random_order: item.randomOrder,
    collaborative_annotation: item.collaborativeAnnotation,
    single_class_classification: item.exclusiveCategories,
    allow_overlapping: item.allowOverlapping,
    grapheme_mode: item.graphemeMode,
    use_relation: item.useRelation,
    tags: item.tags,
    resourcetype: item.resourceType
  }
}

export class APIProjectRepository implements ProjectRepository {
  constructor(private readonly request = ApiService) {}

  async list(query: SearchQuery): Promise<Page<Project>> {
    const fieldMapper = {
      name: 'name',
      createdAt: 'created_at',
      projectType: 'project_type',
      author: 'created_by'
    }
    const sortBy = fieldMapper[query.sortBy]
    const ordering = query.sortDesc ? `-${sortBy}` : `${sortBy}`
    const url = `/projects?limit=${query.limit}&offset=${query.offset}&q=${query.q}&ordering=${ordering}`
    const response = await this.request.get(url)
    return new Page(
      response.data.count,
      response.data.next,
      response.data.previous,
      response.data.results.map((project: { [key: string]: any }) => toModel(project))
    )
  }

  async findById(id: string): Promise<Project> {
    const url = `/projects/${id}`
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async create(item: Project): Promise<Project> {
    const url = `/projects`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async update(item: Project): Promise<void> {
    const url = `/projects/${item.id}`
    const payload = toPayload(item)
    await this.request.patch(url, payload)
  }

  async bulkDelete(projectIds: number[]): Promise<void> {
    const url = `/projects`
    await this.request.delete(url, { ids: projectIds })
  }
}
