import ApiService from '@/services/api.service'
import { Distribution, MyProgress, Percentage, Progress } from '~/domain/models/metrics/metrics'

export interface DisagreementStats {
  categories: string[]
  annotators: string[]
  textTypes: string[]
  perspectives?: string[]
}

export class APIMetricsRepository {
  constructor(private readonly request = ApiService) {}

  async fetchCategoryDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/metrics/category-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchCategoryPercentage(projectId: string): Promise<Percentage> {
    const url = `/projects/${projectId}/metrics/category-percentage`
    const response = await this.request.get(url)
    return response.data
  }


  async fetchSpanDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/metrics/span-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchSpanPercentage(projectId: string): Promise<Percentage> {
    const url = `/projects/${projectId}/metrics/span-percentage`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchRelationDistribution(projectId: string): Promise<Percentage> {
    const url = `/projects/${projectId}/metrics/relation-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchRelationPercentage(projectId: string): Promise<Percentage> {
    const url = `/projects/${projectId}/metrics/relation-percentage`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchMemberProgress(projectId: string): Promise<Progress> {
    const url = `/projects/${projectId}/metrics/member-progress`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchMyProgress(projectId: string): Promise<MyProgress> {
    const url = `/projects/${projectId}/metrics/progress`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchDisagreementStats(projectId: string): Promise<DisagreementStats> {
    const url = `/projects/${projectId}/metrics/disagreement-stats`
    const response = await this.request.get(url)
    return response.data
  }
}
