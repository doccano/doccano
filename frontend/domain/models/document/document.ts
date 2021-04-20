export class DocumentItemList {
  constructor(
    private _count: number,
    private _next: string | null,
    private _prev: string | null,
    private _items: DocumentItem[]
  ) {}

  static valueOf(
    { count, next, previous, results }:
    {
      count   : number,
      next    : string | null,
      previous: string | null,
      results : Array<any>
  }
  ): DocumentItemList {
    const items = results.map(item => DocumentItem.valueOf(item))
    return new DocumentItemList(
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

  get items(): DocumentItem[] {
    return this._items
  }
}

export class DocumentItem {
  constructor(
    public id: number,
    public text: string,
    public meta: string,
    public annotationApprover: boolean | null,
    public commentCount: number
  ) {}

  static valueOf(
    { id, text, meta, annotation_approver, comment_count }:
    { id: number, text: string, meta: string, annotation_approver: boolean | null, comment_count: number }
  ): DocumentItem {
    return new DocumentItem(id, text, meta, annotation_approver, comment_count)
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
