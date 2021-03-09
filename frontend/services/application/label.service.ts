import { LabelItem } from '@/models/label'
import { LabelItemListRepository } from '@/repositories/label/interface'

export class LabelDTO {
  id: number
  text: string
  prefixKey: string | null
  suffixKey: string | null
  backgroundColor: string
  textColor: string

  constructor(item: LabelItem) {
    this.id = item.id
    this.text = item.text
    this.prefixKey = item.prefixKey
    this.suffixKey = item.suffixKey
    this.backgroundColor = item.backgroundColor
    this.textColor = '#ffffff'
  }
}

export class LabelApplicationService {
  constructor(
    private readonly repository: LabelItemListRepository
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
