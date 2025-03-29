import { PerspectiveItem } from '@/domain/models/perspective/perspective'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): PerspectiveItem {
  return {
    id: item.id,
    userId: item.userId,
    projectId: item.projectId,
    subject: item.subject,
    text: item.text,
    category: item.category,
    createdAt: item.createdAt,
    updatedAt: item.updatedAt
  }
}

export class APIPerspectiveRepository {
  constructor(private readonly request = ApiService) {}

async create(projectId: number, data: any): Promise<any> {
    const url = `/projects/${projectId}/perspectives/`;
    const response = await this.request.post(url, data);
    return response.data;
}

  async list(projectId: string, query?: any): Promise<PerspectiveItem[]> {
    const url = `/projects/${projectId}/perspectives`;
    const response = await this.request.get(url, { params: query });
    const data = response.data.results || response.data;
    return data.map((item: any) => toModel(item));
  }
}