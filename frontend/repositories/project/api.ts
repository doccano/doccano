import ApiService from '@/services/api.service'
import { ProjectItem } from '@/models/project'
import { ProjectItemListRepository } from './interface'


export class FromApiProjectItemListRepository implements ProjectItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(): Promise<ProjectItem[]> {
    const url = `/projects`
    const response = await this.request.get(url)
    const responseItems: ProjectItem[] = response.data
    return responseItems.map(item => ProjectItem.valueOf(item))
  }

  async create(item: ProjectItem): Promise<ProjectItem> {
    const url = `/projects`
    const response = await this.request.post(url, item.toObject())
    const responseItem: ProjectItem = response.data
    return ProjectItem.valueOf(responseItem)
  }

  async update(item: ProjectItem): Promise<ProjectItem> {
    const url = `/projects/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    const responseItem: ProjectItem = response.data
    return ProjectItem.valueOf(responseItem)
  }

  async bulkDelete(projectIds: number[]): Promise<void> {
    const url = `/projects`
    await this.request.delete(url, { ids: projectIds })
  }
}
