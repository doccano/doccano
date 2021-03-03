import ApiService from '@/services/api.service'
import { ProjectReadItem, ProjectWriteItem } from '@/models/project'
import { ProjectItemListRepository } from './interface'


export class FromApiProjectItemListRepository implements ProjectItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(): Promise<ProjectReadItem[]> {
    const url = `/projects`
    const response = await this.request.get(url)
    const responseItems: ProjectReadItem[] = response.data
    return responseItems.map(item => ProjectReadItem.valueOf(item))
  }

  async findById(id: string): Promise<ProjectReadItem> {
    const url = `/projects/${id}`
    const response = await this.request.get(url)
    const responseItem: ProjectReadItem = response.data
    return ProjectReadItem.valueOf(responseItem)
  }

  async create(item: ProjectWriteItem): Promise<ProjectReadItem> {
    const url = `/projects`
    const response = await this.request.post(url, item.toObject())
    const responseItem: ProjectReadItem = response.data
    return ProjectReadItem.valueOf(responseItem)
  }

  async update(item: ProjectWriteItem): Promise<void> {
    const url = `/projects/${item.id}`
    const response = await this.request.patch(url, item.toObject())
  }

  async bulkDelete(projectIds: number[]): Promise<void> {
    const url = `/projects`
    await this.request.delete(url, { ids: projectIds })
  }
}
