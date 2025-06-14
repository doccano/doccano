export class Relation {
  constructor(
    readonly id: number,
    readonly fromId: number,
    readonly toId: number,
    private _type: number
  ) {}

  get type(): number {
    return this._type
  }

  changeType(type: number) {
    this._type = type
  }
}
