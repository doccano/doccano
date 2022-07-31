import { LabelDTO } from './labelData'
import { CreateLabelCommand } from './labelCommand'
import { LabelRepository } from '~/domain/models/label/labelRepository'
import { LabelItem } from '~/domain/models/label/label'

export class LabelApplicationService {
  constructor(private readonly repository: LabelRepository) {}

  public async list(id: string): Promise<LabelDTO[]> {
    const items = await this.repository.list(id)
    return items.map((item) => new LabelDTO(item))
  }

  public async findById(projectId: string, labelId: number): Promise<LabelDTO> {
    const item = await this.repository.findById(projectId, labelId)
    return new LabelDTO(item)
  }

  public async create(projectId: string, item: CreateLabelCommand): Promise<LabelDTO> {
    const label = LabelItem.create(item.text, item.prefixKey, item.suffixKey, item.backgroundColor)
    const created = await this.repository.create(projectId, label)
    return new LabelDTO(created)
  }

  public async update(projectId: string, item: LabelDTO): Promise<LabelDTO> {
    const label = new LabelItem(
      item.id,
      item.text,
      item.prefixKey,
      item.suffixKey,
      item.backgroundColor
    )
    const updated = await this.repository.update(projectId, label)
    return new LabelDTO(updated)
  }

  public bulkDelete(projectId: string, items: LabelDTO[]): Promise<void> {
    const ids = items.map((item) => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }

  public async export(projectId: string) {
    const items = await this.repository.list(projectId)
    const labels = items.map((item) => new LabelDTO(item))
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
    await this.repository.uploadFile(projectId, formData)
  }
}
