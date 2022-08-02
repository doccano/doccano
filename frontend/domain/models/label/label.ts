export class LabelItem {
  constructor(
    public id: number,
    public text: string = '',
    public prefixKey: string | null = null,
    public suffixKey: string | null = null,
    public backgroundColor: string = '#73D8FF',
    public textColor: string = '#ffffff'
  ) {}

  static create(
    text: string = '',
    prefixKey: string | null = null,
    suffixKey: string | null = null,
    backgroundColor: string = '#73D8FF'
  ): LabelItem {
    return new LabelItem(0, text, prefixKey, suffixKey, backgroundColor)
  }
}
