import { ProjectReadItem, CurrentUsersRole, ProjectType } from '~/domain/models/project/project'

export class ProjectDTO {
  id: number
  name: string
  description: string
  guideline: string
  current_users_role: CurrentUsersRole
  projectType: ProjectType
  updatedAt: string
  enableRandomOrder: boolean
  enableShareAnnotation: boolean
  singleClassClassification: boolean
  pageLink: string
  tags: Object[]
  canDefineLabel: boolean
  canDefineRelation: boolean
  isTextProject: boolean
  allowOverlapping: boolean
  graphemeMode: boolean

  constructor(item: ProjectReadItem) {
    this.id = item.id
    this.name = item.name
    this.description = item.description
    this.guideline = item.guideline
    this.current_users_role = item.current_users_role
    this.projectType = item.project_type
    this.updatedAt = item.updated_at
    this.enableRandomOrder = item.random_order
    this.enableShareAnnotation = item.collaborative_annotation
    this.singleClassClassification = item.single_class_classification
    this.pageLink = item.annotationPageLink
    this.tags = item.tags
    this.canDefineLabel = item.canDefineLabel
    this.canDefineRelation = item.canDefineRelation
    this.isTextProject = item.isTextProject
    this.allowOverlapping = item.allow_overlapping
    this.graphemeMode = item.grapheme_mode
  }
}

export type ProjectWriteDTO = Pick<ProjectDTO, 'id' | 'name' | 'description' | 'guideline' | 'projectType' | 'enableRandomOrder' | 'enableShareAnnotation' | 'singleClassClassification' | 'allowOverlapping' | 'graphemeMode' | 'tags'>
