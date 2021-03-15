import { LabelItem } from '@/models/label'
import { LabelItemListRepository } from '@/repositories/label/interface'

export class LabelDTO {
  id: number
  text: string
  prefixKey: string | null
  suffixKey: string | null
  backgroundColor: string
  textColor: string

  constructor(item: LabelItem) {
    this.id = item.id
    this.text = item.text
    this.prefixKey = item.prefixKey
    this.suffixKey = item.suffixKey
    this.backgroundColor = item.backgroundColor
    this.textColor = '#ffffff'
  }
}
