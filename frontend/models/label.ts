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

export class LabelItem {
  constructor(
    public id: number,
    public text: string,
    public prefixKey: string | null,
    public suffixKey: string | null,
    public backgroundColor: string,
    public textColor: string = '#ffffff'
  ) {}

  static valueOf(
    { id, text, prefix_key, suffix_key, background_color, text_color }:
    { id: number, text: string, prefix_key: string, suffix_key: string, background_color: string, text_color: string }
  ): LabelItem {
    return new LabelItem(id, text, prefix_key, suffix_key, background_color, text_color)
  }

  get name(): string {
    return this.text
  }

  toObject(): Object {
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
