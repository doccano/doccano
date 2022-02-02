import { ProjectReadItem, ProjectWriteItem, ProjectItemList } from '~/domain/models/project/project'

export type SearchOption = {[key: string]: string | (string | null)[]}

export interface ProjectRepository {
  list({ limit, offset, q }: SearchOption): Promise<ProjectItemList>

  findById(id: string): Promise<ProjectReadItem>

  create(item: ProjectWriteItem): Promise<ProjectReadItem>

  update(item: ProjectWriteItem): Promise<void>

  bulkDelete(projectIds: number[]): Promise<void>
}
