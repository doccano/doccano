import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { ProjectRepository, SearchOption } from '@/domain/models/project/projectRepository'
import { ProjectReadItem, ProjectWriteItem, ProjectItemList } from '~/domain/models/project/project'


export class APIProjectRepository implements ProjectRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list({ limit = '10', offset = '0', q = '' }: SearchOption): Promise<ProjectItemList> {
    const url = `/projects?limit=${limit}&offset=${offset}&q=${q}`
    const response = await this.request.get(url)
    return plainToInstance(ProjectItemList, response.data)
  }

  async findById(id: string): Promise<ProjectReadItem> {
    const url = `/projects/${id}`
    const response = await this.request.get(url)
    return plainToInstance(ProjectReadItem, response.data)
  }

  async create(item: ProjectWriteItem): Promise<ProjectReadItem> {
    const url = `/projects`
    const response = await this.request.post(url, item.toObject())
    return plainToInstance(ProjectReadItem, response.data)
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
