import ApiService from '@/services/api.service'
import { LinkTypesRepository } from "~/domain/models/links/linkTypesRepository";
import { LinkTypeItem } from "~/domain/models/links/link";

export interface LinkTypeResponse {
  id: number,
  name: string,
  color: string
}

export class ApiLinkTypesRepository implements LinkTypesRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<LinkTypeItem[]> {
    const url = `/projects/${projectId}/relation_types`
    const response = await this.request.get(url)
    const responseItems: LinkTypeResponse[] = response.data
    return responseItems.map(item => LinkTypeItem.valueOf(item))
  }

  async create(projectId: string, item: LinkTypeItem): Promise<LinkTypeItem> {
    const url = `/projects/${projectId}/relation_types`
    const response = await this.request.post(url, item.toObject())
    const responseItem: LinkTypeResponse = response.data
    return LinkTypeItem.valueOf(responseItem)
  }

  async update(projectId: string, item: LinkTypeItem): Promise<LinkTypeItem> {
    const url = `/projects/${projectId}/relation_types/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    const responseItem: LinkTypeResponse = response.data
    return LinkTypeItem.valueOf(responseItem)
  }

  async bulkDelete(projectId: string, linkIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/relation_types`
    await this.request.delete(url, { ids: linkIds })
  }
}
