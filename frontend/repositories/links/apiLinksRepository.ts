import ApiService from '@/services/api.service'
import { LinksRepository } from "~/domain/models/links/linksRepository";
import { LinkItem } from "~/domain/models/links/link";

export interface LinkItemResponse {
  id: number,
  text: string,
  prefix_key: string,
  suffix_key: string,
  background_color: string,
  text_color: string
}

export class ApiLinksRepository implements LinksRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<LinkItem[]> {
    const url = `/projects/${projectId}/relation_types`
    const response = await this.request.get(url)
    console.log(response);
    const responseItems: LinkItemResponse[] = response.data
    return responseItems.map(item => LinkItem.valueOf(item))
  }

  async create(projectId: string, item: LinkItem): Promise<LinkItem> {
    const url = `/projects/${projectId}/relation_types`
    const response = await this.request.post(url, item.toObject())
    const responseItem: LinkItemResponse = response.data
    return LinkItem.valueOf(responseItem)
  }

  async update(projectId: string, item: LinkItem): Promise<LinkItem> {
    const url = `/projects/${projectId}/relation_types/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    const responseItem: LinkItemResponse = response.data
    return LinkItem.valueOf(responseItem)
  }

  async bulkDelete(projectId: string, linkIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/relation_types`
    await this.request.delete(url, { ids: linkIds })
  }
}
