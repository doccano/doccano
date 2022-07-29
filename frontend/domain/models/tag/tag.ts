export class TagItem {
  constructor(readonly id: number, readonly text: string, readonly project: string) {}

  toObject(): Object {
    return {
      id: this.id,
      text: this.text,
      project: this.project
    }
  }
}
