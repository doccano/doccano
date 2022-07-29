export class LabelItem {
  constructor(
    readonly id: number,
    readonly text: string,
    readonly prefixKey: string | null,
    readonly suffixKey: string | null,
    readonly backgroundColor: string,
    readonly textColor: string = '#ffffff'
  ) {}
}

export class DocTypeItem extends LabelItem {}
export class SpanTypeItem extends LabelItem {}
