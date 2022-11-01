export class LabelItem {
  constructor(
    readonly id: number,
    readonly text: string,
    readonly prefixKey: string | null,
    readonly suffixKey: string | null,
    readonly backgroundColor: string,
    readonly description: string,
    readonly textColor: string = '#ffffff',
  ) {}

  static create(
    text: string,
    prefixKey: string | null,
    suffixKey: string | null,
    backgroundColor: string,
    description: string,
  ): LabelItem {
    return new LabelItem(0, text, prefixKey, suffixKey, backgroundColor, description)
  }
}
