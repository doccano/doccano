import { ProjectReadItem, ProjectWriteItem } from '@/models/project'


export interface ProjectItemListRepository {
  list(): Promise<ProjectReadItem[]>

  findById(id: string): Promise<ProjectReadItem>

  create(item: ProjectWriteItem): Promise<ProjectReadItem>

  update(item: ProjectWriteItem): Promise<void>

  bulkDelete(projectIds: number[]): Promise<void>
}
