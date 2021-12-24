export class LabelItemList {
  constructor(public labelItems: LabelItem[]) {}

  static valueOf(items: LabelItem[]): LabelItemList {
    return new LabelItemList(items)
  }

  add(item: LabelItem) {
    this.labelItems.push(item)
  }

  update(item: LabelItem) {
    const index = this.labelItems.findIndex(label => label.id === item.id)
    this.labelItems.splice(index, 1, item)
  }

  delete(item: LabelItem) {
    this.labelItems = this.labelItems.filter(label => label.id !== item.id)
  }

  bulkDelete(items: LabelItemList) {
    const ids = items.ids()
    this.labelItems = this.labelItems.filter(label => !ids.includes(label.id))
  }

  count(): Number {
    return this.labelItems.length
  }

  ids(): Number[]{
    return this.labelItems.map(item => item.id)
  }

  get nameList(): string[] {
    return this.labelItems.map(item => item.name)
  }

  get usedKeys(): string[] {
    const items = this.labelItems
                  .filter(item => item.suffixKey !== null)
                  .map(item => item.suffixKey) as string[]
    return items
  }

  toArray(): Object[] {
    return this.labelItems.map(item => item.toObject())
  }
}

interface LabelResponse {
  id: number
  text: string
  prefix_key: string | null
  suffix_key: string | null
  background_color: string
  text_color: string
}

export class LabelItem {
  constructor(
    public id: number,
    public text: string,
    public prefixKey: string | null,
    public suffixKey: string | null,
    public backgroundColor: string,
    public textColor: string = '#ffffff'
  ) {}

  static valueOf(label: LabelResponse): LabelItem {
    return new LabelItem(
      label.id,
      label.text,
      label.prefix_key,
      label.suffix_key,
      label.background_color,
      label.text_color
    )
  }

  get name(): string {
    return this.text
  }

  toObject(): LabelResponse {
    return {
      id: this.id,
      text: this.text,
      prefix_key: this.prefixKey,
      suffix_key: this.suffixKey,
      background_color: this.backgroundColor,
      text_color: this.textColor
    }
  }
}

export class DocTypeItem extends LabelItem {}
export class SpanTypeItem extends LabelItem {}
