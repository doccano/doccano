import 'reflect-metadata'
import { Expose, Type } from 'class-transformer'

export class CommentItem {
  id: number
  user: number
  username: string
  example: number
  text: string

  @Expose({ name: 'created_at' })
  createdAt: string

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

export class CommentItemList {
  count: number
  next: string | null
  prev: string | null

  @Type(() => CommentItem)
  @Expose({ name: 'results' })
  items: CommentItem[]
}
