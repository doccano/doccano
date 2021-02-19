export class LabelItemList {
  constructor(public labelItems: LabelItem[]) {}

  static valueOf(items: LabelItem[]): LabelItemList {
    return new LabelItemList(items)
  }

  get nameList(): string[] {
    return this.labelItems.map(item => item.name)
  }

  toArray(): Object[] {
    return this.labelItems.map(item => item.toObject())
  }
}

export class LabelItem {
  constructor(
    public id: number,
    public text: string,
    public prefixKey: string,
    public suffixKey: string,
    public backgroundColor: string,
    public textColor: string
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
      prefixKey: this.prefixKey,
      suffixKey: this.suffixKey,
      backgroundColor: this.backgroundColor,
      textColor: this.textColor
    }
  }
}
