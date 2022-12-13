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
    return this.fileUrl.slice(l - 1)
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
