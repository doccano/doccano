import { LabelDTO } from './labelData'
import { LabelRepository } from '~/domain/models/label/labelRepository'
import { LabelItem } from '~/domain/models/label/label'


export class LabelApplicationService {
  constructor(
    private readonly repository: LabelRepository
  ) {}

  public async list(id: string): Promise<LabelDTO[]> {
    const items = await this.repository.list(id)
    return items.map(item => new LabelDTO(item))
  }

  public create(projectId: string, item: LabelDTO): void {
    const label = new LabelItem(0, item.text, item.prefixKey, item.suffixKey, item.backgroundColor, item.textColor)
    this.repository.create(projectId, label)
  }

  public update(projectId: string, item: LabelDTO): void {
    const label = new LabelItem(item.id, item.text, item.prefixKey, item.suffixKey, item.backgroundColor, item.textColor)
    this.repository.update(projectId, label)
  }

  public bulkDelete(projectId: string, items: LabelDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }

  public async export(projectId: string) {
    const items = await this.repository.list(projectId)
    const labels = items.map(item => new LabelDTO(item))
    const url = window.URL.createObjectURL(new Blob([JSON.stringify(labels, null, 2)]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `label_config.json`)
    document.body.appendChild(link)
    link.click()
  }

  async upload(projectId: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    await this.repository.uploadFile(projectId, formData)
  }
}
