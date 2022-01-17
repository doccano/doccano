import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { DownloadFormatRepository } from '@/domain/models/download/downloadFormatRepository'
import { Format } from '~/domain/models/download/format'

export class APIDownloadFormatRepository implements DownloadFormatRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<Format[]> {
    const url = `/projects/${projectId}/download-format`
    const response = await this.request.get(url)
    return response.data.map((item: any) => plainToInstance(Format, item))
  }
}
