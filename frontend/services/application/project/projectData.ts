import { ProjectReadItem, ProjectType, ProjectItemList } from '~/domain/models/project/project'

export class ProjectDTO {
  id: number
  name: string
  description: string
  guideline: string
  projectType: ProjectType
  updatedAt: string
  enableRandomOrder: boolean
  enableShareAnnotation: boolean
  singleClassClassification: boolean
  pageLink: string
  tags: Object[] | string[]
  canDefineLabel: boolean
  canDefineRelation: boolean
  isTextProject: boolean
  allowOverlapping: boolean
  graphemeMode: boolean
  hasCategory: boolean
  hasSpan: boolean
  taskNames: string[]
  useRelation: boolean

  constructor(item: ProjectReadItem) {
    this.id = item.id
    this.name = item.name
    this.description = item.description
    this.guideline = item.guideline
    this.projectType = item.projectType
    this.updatedAt = item.updatedAt
    this.enableRandomOrder = item.randomOrder
    this.enableShareAnnotation = item.collaborative_annotation
    this.singleClassClassification = item.exclusiveCategories
    this.pageLink = item.annotationPageLink
    this.tags = item.tags
    this.canDefineLabel = item.canDefineLabel
    this.canDefineRelation = item.canDefineRelation
    this.isTextProject = item.isTextProject
    this.allowOverlapping = item.allowOverlapping
    this.graphemeMode = item.graphemeMode
    this.hasCategory = item.canDefineCategory
    this.hasSpan = item.canDefineSpan
    this.taskNames = item.taskNames
    this.useRelation = item.useRelation
  }
}

export type ProjectWriteDTO = Pick<
  ProjectDTO,
  | 'id'
  | 'name'
  | 'description'
  | 'guideline'
  | 'projectType'
  | 'enableRandomOrder'
  | 'enableShareAnnotation'
  | 'singleClassClassification'
  | 'allowOverlapping'
  | 'graphemeMode'
  | 'useRelation'
> & { tags: string[] }

export class ProjectListDTO {
  count: number
  next: string | null
  prev: string | null
  items: ProjectDTO[]

  constructor(item: ProjectItemList) {
    this.count = item.count
    this.next = item.next
    this.prev = item.prev
    this.items = item.items.map((_) => new ProjectDTO(_))
  }
}
