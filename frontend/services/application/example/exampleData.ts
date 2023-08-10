import { ExampleItem, ExampleItemList, Assignment } from '~/domain/models/example/example'

export class ExampleDTO {
  id: number
  text: string
  meta: object
  annotationApprover: boolean | null
  commentCount: number
  isApproved: boolean
  fileUrl: string
  filename: string
  url: string
  isConfirmed: boolean
  assignments: Assignment[]

  constructor(item: ExampleItem) {
    this.id = item.id
    this.text = item.text
    this.meta = item.meta
    this.annotationApprover = item.annotationApprover
    this.commentCount = item.commentCount
    this.isApproved = !!item.annotationApprover
    this.fileUrl = item.fileUrl
    this.filename = item.filename
    this.url = item.url
    this.isConfirmed = item.isConfirmed
    this.assignments = item.assignments
  }
}

export class ExampleListDTO {
  count: number
  next: string | null
  prev: string | null
  items: ExampleDTO[]

  constructor(item: ExampleItemList) {
    this.count = item.count
    this.next = item.next
    this.prev = item.prev
    this.items = item.items.map((_) => new ExampleDTO(_))
  }
}
