export class BoundingBox {
  constructor(
    readonly id: number,
    readonly uuid: string,
    readonly label: number,
    readonly x: number,
    readonly y: number,
    readonly width: number,
    readonly height: number
  ) {}
}
