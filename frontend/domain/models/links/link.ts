// export class LinkItemList {
//   constructor(public linkItems: LinkTypeItem[]) {}
//
//   static valueOf(items: LinkTypeItem[]): LinkItemList {
//     return new LinkItemList(items)
//   }
//
//   add(item: LinkTypeItem) {
//     this.linkItems.push(item)
//   }
//
//   update(item: LinkTypeItem) {
//     const index = this.linkItems.findIndex(label => label.id === item.id)
//     this.linkItems.splice(index, 1, item)
//   }
//
//   delete(item: LinkTypeItem) {
//     this.linkItems = this.linkItems.filter(label => label.id !== item.id)
//   }
//
//   bulkDelete(items: LinkItemList) {
//     const ids = items.ids()
//     this.linkItems = this.linkItems.filter(label => !ids.includes(label.id))
//   }
//
//   count(): Number {
//     return this.linkItems.length
//   }
//
//   ids(): Number[]{
//     return this.linkItems.map(item => item.id)
//   }
//
//   get nameList(): string[] {
//     return this.linkItems.map(item => item.name)
//   }
//
//   get usedKeys(): string[] {
//     return []
//   }
//
//   toArray(): Object[] {
//     return this.linkItems.map(item => item.toObject())
//   }
// }

export class LinkTypeItem {
    constructor(
        public id: number,
        public name: string,
        public color: string = '#1f1f1f'
    ) {
    }

    static valueOf(
        {id, name, color}:
            { id: number, name: string, color: string }
    ): LinkTypeItem {
        return new LinkTypeItem(id, name, color)
    }

    toObject(): Object {
        return {
            id: this.id,
            name: this.name,
            color: this.color
        }
    }
}

export class LinkItem {
    constructor(
        public id: number,
        public annotation_id_1: number,
        public annotation_id_2: number,
        public type: number
    ) {
    }

    static valueOf(
        {id, annotation_id_1, annotation_id_2, type}:
            { id: number, annotation_id_1: number, annotation_id_2: number, type: number }
    ): LinkItem {
        return new LinkItem(id, annotation_id_1, annotation_id_2, type)
    }

    toObject(): Object {
        return {
            id: this.id,
            annotation_id_1: this.annotation_id_1,
            annotation_id_2: this.annotation_id_2,
            type: this.type
        }
    }
}
