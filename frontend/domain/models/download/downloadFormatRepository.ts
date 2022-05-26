import { Format } from './format'

export interface DownloadFormatRepository {
  list(projectId: string): Promise<Format[]>
}
