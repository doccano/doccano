export class CommentItem {
  constructor(
    readonly id: number,
    readonly user: number,
    readonly username: string,
    readonly example: number,
    readonly text: string,
    readonly createdAt: string
  ) {}

  by(userId: number) {
    return this.user === userId
  }
}

export class CommentItemList {
  constructor(
    readonly count: number,
    readonly next: string | null,
    readonly prev: string | null,
    readonly items: CommentItem[]
  ) {}
}
