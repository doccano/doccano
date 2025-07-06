import ApiService from '@/services/api.service'
import { Distribution, MyProgress, Progress } from '~/domain/models/metrics/metrics'

export class APIMetricsRepository {
  constructor(private readonly request = ApiService) {}

  async fetchCategoryDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/metrics/category-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchSpanDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/metrics/span-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchRelationDistribution(projectId: string): Promise<Distribution> {
    const url = `/projects/${projectId}/metrics/relation-distribution`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchDiscrepancyStats(projectId: string, params: any = {}): Promise<any> {
    const url = `/projects/${projectId}/metrics/discrepancy-stats`
    const response = await this.request.get(url, { params })
    return response.data
  }

  async fetchPerspectiveStats(projectId: string, params: any = {}): Promise<any> {
    const url = `/projects/${projectId}/metrics/perspective-stats`
    const response = await this.request.get(url, { params })
    return response.data
  }

  async fetchLabelStats(projectId: string, params: any = {}): Promise<any> {
    const url = `/projects/${projectId}/metrics/label-stats`
    const response = await this.request.get(url, { params })
    return response.data
  }

  async fetchDatasetDetails(projectId: string, params: any = {}): Promise<any> {
    const url = `/projects/${projectId}/metrics/dataset-details`
    const response = await this.request.get(url, { params })
    return response.data
  }

  async fetchDatasetTexts(projectId: string): Promise<any> {
    const url = `/projects/${projectId}/metrics/dataset-texts`
    const response = await this.request.get(url)
    return response.data
  }

  async fetchPerspectiveAnswers(projectId: string, questionId: string): Promise<any> {
    const url = `/projects/${projectId}/metrics/perspective-answers/${questionId}`
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
}
