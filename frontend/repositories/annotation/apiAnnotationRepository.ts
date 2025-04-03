import { Annotation } from '@/domain/models/annotation/annotation'
import ApiService from '@/services/api.service'

function simpleHash(str: string): string {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
  }
  return hash.toString(16);
}

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

  async listSimilar(projectId: number): Promise<any[]> {
    // Fetch all annotations for the given project.
    // Adjust the parameter key 'project' if your API expects something different.
    const url = `/annotations/`
    const response = await ApiService.get(url, { params: { project: projectId } })
    const annotations: Annotation[] = response.data.results || response.data

    // Group annotations by a signature computed from text and label (ignoring spans)
    const groups: { [signature: string]: any } = {}
    for (const annotation of annotations) {
      const extracted = annotation.extracted_labels
      if (!extracted || !extracted.text || !extracted.label) continue

      const signatureData = {
        text: extracted.text,
        label: extracted.label
      }
      const signatureString = JSON.stringify(signatureData, Object.keys(signatureData).sort())
      const signature = simpleHash(signatureString)

      if (!groups[signature]) {
        groups[signature] = {
          signature,
          snippet: extracted.text.substring(0, 100),
          labels: [extracted.label],
          annotations: []
        }
      }
      groups[signature].annotations.push(annotation)
    }
    
    const result: any[] = []
    for (const key in groups) {
      const group = groups[key]
      if (group.annotations.length < 2) continue

      let spansDiffer = false
      for (let i = 0; i < group.annotations.length; i++) {
        for (let j = i + 1; j < group.annotations.length; j++) {
          const spans1 = group.annotations[i].extracted_labels.spans
          const spans2 = group.annotations[j].extracted_labels.spans
          if (JSON.stringify(spans1) !== JSON.stringify(spans2)) {
            spansDiffer = true
            break
          }
        }
        if (spansDiffer) break
      }
      if (spansDiffer) {
        result.push({
          signature: group.signature,
          snippet: group.snippet,
          labels: group.labels,
          count: group.annotations.length,
          annotations: group.annotations
        })
      }
    }

    return result
  }

  async deleteAllAnnotations(projectId: number): Promise<void> {
    const annotations = await this.list({ project: projectId });
    await Promise.all(annotations.map(annotation => this.delete(annotation.id)));
  }
}