export class TextLabel {
  constructor(readonly id: number, private _text: string, readonly user: number) {}

  get text(): string {
    return this._text
  }

  updateText(text: string) {
    this._text = text
  }
}
