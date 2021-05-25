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
        public type: number,
        public user: number,
        public timestamp: string
    ) {
    }

    static valueOf(
        {id, annotation_id_1, annotation_id_2, type, user, timestamp}:
            { id: number, annotation_id_1: number, annotation_id_2: number, type: number, user:number, timestamp:string }
    ): LinkItem {
        return new LinkItem(id, annotation_id_1, annotation_id_2, type, user, timestamp)
    }

    toObject(): Object {
        return {
            id: this.id,
            annotation_id_1: this.annotation_id_1,
            annotation_id_2: this.annotation_id_2,
            type: this.type,
            user: this.user,
            timestamp: this.timestamp
        }
    }
}
