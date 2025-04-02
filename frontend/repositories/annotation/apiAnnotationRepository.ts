import { Annotation } from '@/domain/models/annotation/annotation'
import ApiService from '@/services/api.service'

export class APIAnnotationRepository {
  async list(query?: any): Promise<Annotation[]> {
    const url = `/annotations/`
    const response = await ApiService.get(url, { params: query })
    return response.data.results || response.data
  }

  async create(data: any): Promise<Annotation> {
    const url = `/annotations/`
    const response = await ApiService.post(url, data)
    return response.data
  }

  async update(annotationId: number, data: any, options?: { method?: 'patch' | 'put' }): Promise<Annotation> {
    const url = `/annotations/${annotationId}/`
    if (options && options.method === 'put') {
      const response = await ApiService.put(url, data)
      return response.data
    } else {
      const response = await ApiService.patch(url, data)
      return response.data
    }
  }

  async delete(annotationId: number): Promise<void> {
    const url = `/annotations/${annotationId}/`
    await ApiService.delete(url)
  }

  async getByDatasetItem(dataset_item_id: number): Promise<Annotation | null> {
    const url = `/annotations/`
    const response = await ApiService.get(url, {
      params: { dataset_item_id }
    })
    const annotations: Annotation[] = response.data.results || response.data
    return annotations.length > 0 ? annotations[0] : null
  }
}