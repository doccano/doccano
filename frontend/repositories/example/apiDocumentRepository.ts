import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { ExampleRepository, SearchOption } from '~/domain/models/example/exampleRepository'
import { ExampleItem, ExampleItemList } from '~/domain/models/example/example'

export class APIExampleRepository implements ExampleRepository {
  constructor(private readonly request = ApiService) {}

  async list(
    projectId: string,
    { limit = '10', offset = '0', q = '', isChecked = '' }: SearchOption
  ): Promise<ExampleItemList> {
    const url = `/projects/${projectId}/examples?limit=${limit}&offset=${offset}&q=${q}&confirmed=${isChecked}`
    const response = await this.request.get(url)
    return plainToInstance(ExampleItemList, response.data)
  }

  async create(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/examples`
    const response = await this.request.post(url, item.toObject())
    return plainToInstance(ExampleItem, response.data)
  }

  async update(projectId: string, item: ExampleItem): Promise<ExampleItem> {
    const url = `/projects/${projectId}/examples/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    return plainToInstance(ExampleItem, response.data)
  }

  async bulkDelete(projectId: string, ids: number[]): Promise<void> {
    const url = `/projects/${projectId}/examples`
    await this.request.delete(url, { ids })
  }

  async deleteAll(projectId: string): Promise<void> {
    const url = `/projects/${projectId}/examples`
    await this.request.delete(url)
  }

  async findById(projectId: string, exampleId: number): Promise<ExampleItem> {
    const url = `/projects/${projectId}/examples/${exampleId}`
    const response = await this.request.get(url)
    return plainToInstance(ExampleItem, response.data)
  }

  async confirm(projectId: string, exampleId: number): Promise<void> {
    const url = `/projects/${projectId}/examples/${exampleId}/states`
    await this.request.post(url, {})
  }
}
