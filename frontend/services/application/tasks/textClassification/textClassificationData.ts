import { TextClassificationItem } from '~/domain/models/tasks/textClassification'


export class TextClassificationDTO {
  id: number;
  label: number;
  user: number;

  constructor(item: TextClassificationItem) {
    this.id = item.id;
    this.label = item.label;
    this.user = item.user;
  }
}
