import { ProjectItem } from '@/models/project'


export interface ProjectItemListRepository {
  list(): Promise<ProjectItem[]>

  create(item: ProjectItem): Promise<ProjectItem>

  update(item: ProjectItem): Promise<ProjectItem>

  bulkDelete(projectIds: number[]): Promise<void>
}
