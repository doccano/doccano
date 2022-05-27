export class TagItem {
  id: number
  text: string
  project: string

  toObject(): Object {
    return {
      id: this.id,
      text: this.text,
      project: this.project
    }
  }
}
