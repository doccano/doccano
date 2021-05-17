import { DocumentItem, DocumentItemList } from '~/domain/models/document/document'


export class DocumentDTO {
  id: number;
  text: string;
  meta: object;
  annotationApprover: boolean | null;
  commentCount: number;
  isApproved: boolean;
  fileUrl: string;
  filename: string;
  url: string;

  constructor(item: DocumentItem) {
    this.id = item.id
    this.text = item.text
    this.meta = item.meta
    this.annotationApprover = item.annotationApprover
    this.commentCount = item.commentCount
    this.isApproved = !!item.annotationApprover
    this.fileUrl = item.fileUrl
    this.filename = item.filename
    this.url = item.url
  }
}

export class DocumentListDTO {
  count: number
  next : string | null
  prev : string | null
  items: DocumentDTO[]

  constructor(item: DocumentItemList) {
    this.count = item.count
    this.next = item.next
    this.prev = item.prev
    this.items = item.items.map(_ => new DocumentDTO(_))
  }
}
