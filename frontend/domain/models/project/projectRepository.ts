import { ProjectReadItem, ProjectWriteItem, ProjectItemList } from '~/domain/models/project/project'

const sortableFieldList = ['name', 'projectType', 'createdAt', 'author'] as const
type SortableFields = typeof sortableFieldList[number]

export class SearchQuery {
  readonly limit: number = 10
  readonly offset: number = 0
  readonly q: string = ''
  readonly sortBy: SortableFields = 'createdAt'
  readonly sortDesc: boolean = false

  constructor(_limit: string, _offset: string, _q?: string, _sortBy?: string, _sortDesc?: string) {
    this.limit = /^\d+$/.test(_limit) ? parseInt(_limit) : 10
    this.offset = /^\d+$/.test(_offset) ? parseInt(_offset) : 0
    this.q = _q || ''
    this.sortBy = (
      _sortBy && sortableFieldList.includes(_sortBy as SortableFields) ? _sortBy : 'createdAt'
    ) as SortableFields
    this.sortDesc = _sortDesc === 'true'
  }
}

export interface ProjectRepository {
  list(query: SearchQuery): Promise<ProjectItemList>

  findById(id: string): Promise<ProjectReadItem>

  create(item: ProjectWriteItem): Promise<ProjectReadItem>

  update(item: ProjectWriteItem): Promise<void>

  bulkDelete(projectIds: number[]): Promise<void>
}
