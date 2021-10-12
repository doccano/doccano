import { CommentItem } from '~/domain/models/comment/comment'


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
