export class ExampleItem {
  constructor(
    readonly id: number,
    readonly text: string,
    readonly meta: object,
    readonly annotationApprover: boolean | null,
    readonly commentCount: number,
    readonly fileUrl: string,
    readonly isConfirmed: boolean,
    readonly filename: string
  ) {}

  get url() {
    const l = this.fileUrl.indexOf('media/')
    const r = this.fileUrl.indexOf('media/', l + 1)
    return this.fileUrl.slice(0, l) + this.fileUrl.slice(r)
  }
}

export class ExampleItemList {
  constructor(
    readonly count: number,
    readonly next: string | null,
    readonly prev: string | null,
    readonly items: ExampleItem[]
  ) {}
}
