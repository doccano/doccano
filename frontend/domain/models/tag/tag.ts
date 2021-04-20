export class TagItemList {
  constructor(public tagItems: TagItem[]) {}

  static valueOf(items: TagItem[]): TagItemList {
    return new TagItemList(items)
  }

  add(item: TagItem) {
    this.tagItems.push(item)
  }

  delete(item: TagItem) {
    this.tagItems = this.tagItems.filter(tag => tag.id !== item.id)
  }

  ids(): Number[]{
    return this.tagItems.map(item => item.id)
  }

  toArray(): Object[] {
    return this.tagItems.map(item => item.toObject())
  }
}

export class TagItem {
  constructor(
    public id: number,
    public text: string,
    public project: string
  ) {}

  static valueOf(
    { id, text, project }:
    { id: number, text: string, project: string }
  ): TagItem {
    return new TagItem(id, text, project)
  }

  toObject(): Object {
    return {
      id: this.id,
      text: this.text,
      project: this.project
    }
  }
}
