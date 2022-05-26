import 'reflect-metadata'
import { Expose, Type } from 'class-transformer'

export class ExampleItem {
  id: number
  text: string
  meta: object

  @Expose({ name: 'annotation_approver' })
  annotationApprover: boolean | null

  @Expose({ name: 'comment_count' })
  commentCount: number

  @Expose({ name: 'filename' })
  fileUrl: string

  @Expose({ name: 'is_confirmed' })
  isConfirmed: boolean

  @Expose({ name: 'upload_name' })
  filename: string

  get url() {
    const l = this.fileUrl.indexOf('media/')
    const r = this.fileUrl.indexOf('media/', l + 1)
    return this.fileUrl.slice(0, l) + this.fileUrl.slice(r)
  }

  toObject(): Object {
    return {
      id: this.id,
      text: this.text,
      meta: this.meta,
      annotation_approver: this.annotationApprover,
      comment_count: this.commentCount
    }
  }
}

export class ExampleItemList {
  count: number
  next: string | null
  prev: string | null

  @Type(() => ExampleItem)
  @Expose({ name: 'results' })
  items: ExampleItem[]
}
