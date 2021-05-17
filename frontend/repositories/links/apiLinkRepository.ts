import ApiService from '@/services/api.service'
import { LinkRepository } from "~/domain/models/links/linkRepository";
import { LinkItem } from "~/domain/models/links/link";

export interface LinkResponse {
  id: number
  annotation_id_1: number
  annotation_id_2: number
  type: number
}

export class ApiLinkRepository implements LinkRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async create(projectId: string, item: LinkItem): Promise<LinkItem> {
    const url = `/projects/${projectId}/annotation_relations`
    const response = await this.request.post(url, item.toObject())
    const responseItem: LinkResponse = response.data
    return LinkItem.valueOf(responseItem)
  }

  async update(projectId: string, item: LinkItem): Promise<LinkItem> {
    const url = `/projects/${projectId}/annotation_relations/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    const responseItem: LinkResponse = response.data
    return LinkItem.valueOf(responseItem)
  }

  async bulkDelete(projectId: string, linkIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/annotation_relations`
    await this.request.delete(url, { ids: linkIds })
  }
}
