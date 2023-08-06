export interface Assignment {
  id: string
  assignee: string
  assignee_id: number
}

export class ExampleItem {
  constructor(
    readonly id: number,
    readonly text: string,
    readonly meta: object,
    readonly annotationApprover: boolean | null,
    readonly commentCount: number,
    readonly fileUrl: string,
    readonly isConfirmed: boolean,
    readonly filename: string,
    readonly assignments: Assignment[]
  ) {}

  get url() {
    const l = this.fileUrl.indexOf('/media/')
    if (l < 0) {
      return this.fileUrl
    }
    return this.fileUrl.slice(l)
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
