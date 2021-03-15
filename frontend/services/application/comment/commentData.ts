import { CommentItem } from '~/domain/models/comment/comment'


export class CommentReadDTO {
  id: number;
  user: number;
  username: string;
  documentText: string;
  text: string;
  createdAt: string;

  constructor(item: CommentItem) {
    this.id = item.id;
    this.user = item.user;
    this.username = item.username;
    this.documentText = item.documentText;
    this.text = item.text;
    this.createdAt = item.createdAt;
  }
}
