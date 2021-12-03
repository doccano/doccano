import { CommentItem, CommentItemList } from '~/domain/models/comment/comment'


export class CommentReadDTO {
  id: number;
  user: number;
  username: string;
  example: number;
  text: string;
  createdAt: string;

  constructor(item: CommentItem) {
    this.id = item.id;
    this.user = item.user;
    this.username = item.username;
    this.example = item.example;
    this.text = item.text;
    this.createdAt = item.createdAt;
  }
}

export class CommentListDTO {
  count: number
  next : string | null
  prev : string | null
  items: CommentReadDTO[]

  constructor(item: CommentItemList) {
    this.count = item.count
    this.next = item.next
    this.prev = item.prev
    this.items = item.items.map(_ => new CommentReadDTO(_))
  }
}
