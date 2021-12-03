export class CommentItemList {
  constructor(
    private _count: number,
    private _next: string | null,
    private _prev: string | null,
    private _items: CommentItem[]
  ) {}

  static valueOf(
    { count, next, previous, results }:
    {
      count   : number,
      next    : string | null,
      previous: string | null,
      results : Array<any>
  }
  ): CommentItemList {
    const items = results.map(item => CommentItem.valueOf(item))
    return new CommentItemList(
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

  get items(): CommentItem[] {
    return this._items
  }
}

export class CommentItem {
  constructor(
    public id: number,
    public user: number,
    public username: string,
    public example: number,
    public text: string,
    public createdAt: string
  ) {}

  static valueOf(
    { id, user, username, example, text, created_at }:
    { id: number, user: number, username: string, example: number,
      text: string, created_at: string }
  ): CommentItem {
    return new CommentItem(id, user, username, example, text, created_at)
  }

  by(userId: number) {
    return this.user === userId
  }

  toObject(): Object {
    return {
      id: this.id,
      user: this.user,
      username: this.username,
      document: this.example,
      text: this.text,
      created_at: this.createdAt
    }
  }
}
