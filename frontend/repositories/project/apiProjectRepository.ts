import ApiService from '@/services/api.service'
import { ProjectRepository, SearchOption } from '@/domain/models/project/projectRepository'
import { ProjectReadItem, ProjectWriteItem, ProjectItemList } from '@/domain/models/project/project'

function toModel(item: { [key: string]: any }): ProjectReadItem {
  return new ProjectReadItem(
    item.id,
    item.name,
    item.description,
    item.guideline,
    item.users,
    item.tags,
    item.project_type,
    item.updated_at,
    item.random_order,
    item.collaborative_annotation,
    item.single_class_classification,
    item.resourcetype,
    item.allow_overlapping,
    item.grapheme_mode,
    item.use_relation,
    item.is_text_project,
    item.can_define_label,
    item.can_define_relation,
    item.can_define_span,
    item.can_define_category
  )
}

function toPayload(item: ProjectWriteItem): { [key: string]: any } {
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
    tags: item.tags.map((tag) => ({ text: tag })),
    resourcetype: item.resourceType
  }
}

export class APIProjectRepository implements ProjectRepository {
  constructor(private readonly request = ApiService) {}

  async list({ limit = '10', offset = '0', q = '' }: SearchOption): Promise<ProjectItemList> {
    const url = `/projects?limit=${limit}&offset=${offset}&q=${q}`
    const response = await this.request.get(url)
    return new ProjectItemList(
      response.data.count,
      response.data.next,
      response.data.previous,
      response.data.results.map((project: { [key: string]: any }) => toModel(project))
    )
  }

  async findById(id: string): Promise<ProjectReadItem> {
    const url = `/projects/${id}`
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async create(item: ProjectWriteItem): Promise<ProjectReadItem> {
    const url = `/projects`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async update(item: ProjectWriteItem): Promise<void> {
    const url = `/projects/${item.id}`
    const payload = toPayload(item)
    await this.request.patch(url, payload)
  }

  async bulkDelete(projectIds: number[]): Promise<void> {
    const url = `/projects`
    await this.request.delete(url, { ids: projectIds })
  }
}
