export class CommentItemList {
  constructor(public commentItems: CommentItem[]) {}

  static valueOf(items: CommentItem[]): CommentItemList {
    return new CommentItemList(items)
  }

  add(item: CommentItem) {
    this.commentItems.push(item)
  }

  update(item: CommentItem) {
    const index = this.commentItems.findIndex(comment => comment.id === item.id)
    this.commentItems.splice(index, 1, item)
  }

  delete(item: CommentItem) {
    this.commentItems = this.commentItems.filter(comment => comment.id !== item.id)
  }

  deleteBulk(items: CommentItemList) {
    const ids = items.ids()
    this.commentItems = this.commentItems.filter(comment => !ids.includes(comment.id))
  }

  count(): Number {
    return this.commentItems.length
  }

  ids(): Number[]{
    return this.commentItems.map(item => item.id)
  }

  toArray(): Object[] {
    return this.commentItems.map(item => item.toObject())
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
