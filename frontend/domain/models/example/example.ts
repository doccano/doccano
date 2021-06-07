export class ExampleItemList {
  constructor(
    private _count: number,
    private _next: string | null,
    private _prev: string | null,
    private _items: ExampleItem[]
  ) {}

  static valueOf(
    { count, next, previous, results }:
    {
      count   : number,
      next    : string | null,
      previous: string | null,
      results : Array<any>
  }
  ): ExampleItemList {
    const items = results.map(item => ExampleItem.valueOf(item))
    return new ExampleItemList(
      count,
      next,
      previous,
      items
    )
  }

  get count() {
    return this._count
  }

  get next() {
    return this._next
  }

  get prev() {
    return this._prev
  }

  get items(): ExampleItem[] {
    return this._items
  }
}

export class ExampleItem {
  constructor(
    public id: number,
    public text: string,
    public meta: object,
    public annotationApprover: boolean | null,
    public commentCount: number,
    public fileUrl: string,
    public isConfirmed: boolean
  ) {}

  static valueOf(
    { id, text, meta, annotation_approver, comment_count, filename, is_confirmed }:
    {
      id: number,
      text: string,
      meta: object,
      annotation_approver: boolean | null,
      comment_count: number,
      filename: string,
      is_confirmed: boolean
  }
  ): ExampleItem {
    return new ExampleItem(id, text, meta, annotation_approver, comment_count, filename, is_confirmed)
  }

  get url() {
    const l = this.fileUrl.indexOf('media/')
    const r = this.fileUrl.indexOf('media/', l + 1)
    return this.fileUrl.slice(0, l) + this.fileUrl.slice(r)
  }

  get filename() {
    const items = this.fileUrl.split('/')
    return items[items.length - 1]
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
