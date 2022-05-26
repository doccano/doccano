import { CategoryItem } from '~/domain/models/tasks/textClassification'

export class TextClassificationDTO {
  id: number
  label: number
  user: number

  constructor(item: CategoryItem) {
    this.id = item.id
    this.label = item.label
    this.user = item.user
  }
}
