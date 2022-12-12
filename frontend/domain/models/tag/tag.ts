export class TagItem {
  constructor(readonly id: number, readonly text: string, readonly project: string | number) {}

  static create(text: string): TagItem {
    return new TagItem(0, text, 0)
  }
}
