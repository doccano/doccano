export class TextLabel {
  constructor(readonly id: number, private _text: string, readonly user: number) {}

  public static create(text: string): TextLabel {
    return new TextLabel(0, text, 0)
  }

  get text(): string {
    return this._text
  }

  updateText(text: string) {
    this._text = text
  }
}
