export class LabelItem {
  constructor(
    readonly id: number,
    readonly text: string,
    readonly prefixKey: string | null,
    readonly suffixKey: string | null,
    readonly backgroundColor: string,
    readonly project_id: number,
    readonly textColor: string = '#ffffff'
  ) {}

  static create(
    text: string,
    prefixKey: string | null,
    suffixKey: string | null,
    backgroundColor: string,
    project_id: number
  ): LabelItem {
    return new LabelItem(0, text, prefixKey, suffixKey, backgroundColor, project_id)
  }
}
