import ApiService from '@/services/api.service'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'

function toModel(item: { [key: string]: any }): PerspectiveItem {
  return new PerspectiveItem(item.id, item.project_id, item.questions, item.members)
}

function toPayload(item: PerspectiveItem): { [key: string]: any } {
  return {
    id: item.id,
    project_id: item.project_id,
    questions: item.questions,
    members: item.members
  }
}

export class APIPerspectiveRepository {
  constructor(private readonly baseUrl = 'perspective', private readonly request = ApiService) {}

  async list(username?: string): Promise<PerspectiveItem[]> {
    let url = `/${this.baseUrl}s`

    if (username) {
      url += `?search=${encodeURIComponent(username)}`
    }

    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, item: PerspectiveItem): Promise<PerspectiveItem> {
    const url = `/projects/${projectId}/${this.baseUrl}s/create`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }
}
