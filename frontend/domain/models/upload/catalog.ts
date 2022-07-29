export class Catalog {
  constructor(
    readonly name: string,
    readonly example: string,
    readonly properties: object,
    readonly taskId: string,
    readonly displayName: string,
    readonly acceptTypes: string
  ) {}
}
