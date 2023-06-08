import { Page } from '~/domain/models/page'
import { Project } from '~/domain/models/project/project'
import { TagItem } from '~/domain/models/tag/tag'
import { APIProjectRepository, SearchQuery } from '~/repositories/project/apiProjectRepository'

type ProjectFields = {
  name: string
  description: string
  guideline: string
  projectType: string
  enableRandomOrder: boolean
  enableSharingMode: boolean
  exclusiveCategories: boolean
  tags: string[]
  allowOverlappingSpans: boolean
  enableGraphemeMode: boolean
  useRelation: boolean
  allowMemberToCreateLabelType: boolean
}

export interface SearchQueryData {
  limit: string
  offset: string
  q?: string
  sortBy?: string
  sortDesc?: string
}

export class ProjectApplicationService {
  constructor(private readonly repository: APIProjectRepository) {}

  public async list(q: SearchQueryData): Promise<Page<Project>> {
    try {
      const query = new SearchQuery(q.limit, q.offset, q.q, q.sortBy, q.sortDesc)
      return await this.repository.list(query)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async findById(id: string): Promise<Project> {
    return await this.repository.findById(id)
  }

  public async create({
    name,
    description,
    projectType,
    enableRandomOrder,
    enableSharingMode,
    exclusiveCategories,
    allowOverlappingSpans,
    enableGraphemeMode,
    useRelation,
    tags,
    guideline = '',
    allowMemberToCreateLabelType = false
  }: ProjectFields): Promise<Project> {
    const project = Project.create(
      0,
      name,
      description,
      guideline,
      projectType,
      enableRandomOrder,
      enableSharingMode,
      exclusiveCategories,
      allowOverlappingSpans,
      enableGraphemeMode,
      useRelation,
      tags.map((tag) => TagItem.create(tag)),
      allowMemberToCreateLabelType
    )
    try {
      return await this.repository.create(project)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(
    projectId: number,
    {
      name,
      description,
      projectType,
      enableRandomOrder,
      enableSharingMode,
      exclusiveCategories,
      allowOverlappingSpans,
      enableGraphemeMode,
      useRelation,
      guideline = '',
      allowMemberToCreateLabelType
    }: Omit<ProjectFields, 'tags'>
  ): Promise<void> {
    const project = Project.create(
      projectId,
      name,
      description,
      guideline,
      projectType,
      enableRandomOrder,
      enableSharingMode,
      exclusiveCategories,
      allowOverlappingSpans,
      enableGraphemeMode,
      useRelation,
      [],
      allowMemberToCreateLabelType
    )

    try {
      await this.repository.update(project)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(projects: Project[]): Promise<void> {
    const ids = projects.map((project) => project.id)
    return this.repository.bulkDelete(ids)
  }

  public async clone(project: Project): Promise<Project> {
    try {
      return await this.repository.clone(project)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }
}
