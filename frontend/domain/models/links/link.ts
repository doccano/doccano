export class LinkItemList {
  constructor(public LinkItems: LinkItem[]) {}

  static valueOf(items: LinkItem[]): LinkItemList {
    return new LinkItemList(items)
  }

  add(item: LinkItem) {
    this.LinkItems.push(item)
  }

  update(item: LinkItem) {
    const index = this.LinkItems.findIndex(label => label.id === item.id)
    this.LinkItems.splice(index, 1, item)
  }

  delete(item: LinkItem) {
    this.LinkItems = this.LinkItems.filter(label => label.id !== item.id)
  }

  bulkDelete(items: LinkItemList) {
    const ids = items.ids()
    this.LinkItems = this.LinkItems.filter(label => !ids.includes(label.id))
  }

  count(): Number {
    return this.LinkItems.length
  }

  ids(): Number[]{
    return this.LinkItems.map(item => item.id)
  }

  get nameList(): string[] {
    return this.LinkItems.map(item => item.name)
  }

  get usedKeys(): string[] {
    const items = this.LinkItems
                  .filter(item => item.suffixKey !== null)
                  .map(item => item.suffixKey) as string[]
    return items
  }

  toArray(): Object[] {
    return this.LinkItems.map(item => item.toObject())
  }
}

export class LinkItem {
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
  ): LinkItem {
    return new LinkItem(id, text, prefix_key, suffix_key, background_color, text_color)
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
