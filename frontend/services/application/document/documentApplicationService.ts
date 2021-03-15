import { DocumentDTO, DocumentListDTO } from './documentData'
import { DocumentRepository, SearchOption } from '~/domain/models/document/documentRepository'
import { DocumentItem } from '~/domain/models/document/document'


export class DocumentApplicationService {
  constructor(
    private readonly repository: DocumentRepository
  ) {}

  public async list(projectId: string, options: SearchOption): Promise<DocumentListDTO> {
    try {
      const item = await this.repository.list(projectId, options)
      return new DocumentListDTO(item)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async fetchOne(projectId: string, page: string, q: string, isChecked: string, filterName: string): Promise<DocumentListDTO> {
    const offset = (parseInt(page, 10) - 1).toString()
    const options: SearchOption = {
      limit: '1',
      offset,
      q,
      isChecked,
      filterName
    }
    return await this.list(projectId, options)
  }

  public async create(projectId: string, item: DocumentDTO): Promise<DocumentDTO> {
    try {
      const doc = this.toModel(item)
      const response = await this.repository.create(projectId, doc)
      return new DocumentDTO(response)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(projectId: string, item: DocumentDTO): Promise<void> {
    try {
      const doc = this.toModel(item)
      await this.repository.update(projectId, doc)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(projectId: string, items: DocumentDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }

  public async download(
    projectId: string, filename: string, format: any, onlyApproved: boolean
  ): Promise<void> {
    const response = await this.repository.exportFile(projectId, format.type, onlyApproved)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${filename}.${format.extension}`)
    document.body.appendChild(link)
    link.click()
  }

  public async upload(projectId: string, file: File, format: string): Promise<void> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('format', format)
    const response = await this.repository.uploadFile(projectId, formData)
  }

  public async approve(projectId: string, docId: number, approved: boolean): Promise<void> {
    await this.repository.approve(projectId, docId, approved)
  }

  private toModel(item: DocumentDTO): DocumentItem {
    return new DocumentItem(
      item.id,
      item.text,
      item.meta,
      item.annotationApprover,
      item.commentCount
    )
  }
}
