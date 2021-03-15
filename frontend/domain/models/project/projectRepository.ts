import { ProjectReadItem, ProjectWriteItem } from '~/domain/models/project/project'


export interface ProjectRepository {
  list(): Promise<ProjectReadItem[]>

  findById(id: string): Promise<ProjectReadItem>

  create(item: ProjectWriteItem): Promise<ProjectReadItem>

  update(item: ProjectWriteItem): Promise<void>

  bulkDelete(projectIds: number[]): Promise<void>
}
