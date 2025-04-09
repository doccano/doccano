import { Disagreement } from '@/domain/models/disagreement/disagreement'
import ApiService from '@/services/api.service'

export class APIDisagreementRepository {
  async list(projectId: number, query?: any): Promise<Disagreement[]> {
    const url = `/projects/${projectId}/disagreements`
    const response = await ApiService.get(url, { params: query })
    return response.data.results || response.data
  }

  async create(projectId: number, data: any): Promise<Disagreement> {
    const url = `/projects/${projectId}/disagreements`
    const response = await ApiService.post(url, data)
    return response.data
  }

  async update(projectId: number, disagreementId: number, data: any): Promise<Disagreement> {
    const url = `/projects/${projectId}/disagreements/${disagreementId}/`
    const response = await ApiService.patch(url, data)
    return response.data
  }

  async delete(projectId: number, disagreementId: number): Promise<void> {
    const url = `/projects/${projectId}/disagreements/${disagreementId}/`
    await ApiService.delete(url)
  }
}