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
        public fromId: number,
        public toId: number,
        public type: number,
    ) {
    }

    static valueOf(
        {id, from_id, to_id, type}: { id: number, from_id: number, to_id: number, type: number }
    ): LinkItem {
        return new LinkItem(id, from_id, to_id, type)
    }

    toObject(): Object {
        return {
            id: this.id,
            from_id: this.fromId,
            to_id: this.toId,
            type: this.type,
        }
    }
}
