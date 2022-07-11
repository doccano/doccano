export class BoundingBoxItem {
  constructor(
    public id: number,
    public uuid: string,
    public label: number,
    public x: number,
    public y: number,
    public width: number,
    public height: number
  ) {}

  static valueOf({
    id,
    uuid,
    label,
    x,
    y,
    width,
    height
  }: {
    id: number
    uuid: string
    label: number
    x: number
    y: number
    width: number
    height: number
  }): BoundingBoxItem {
    return new BoundingBoxItem(id, uuid, label, x, y, width, height)
  }

  toObject(): Object {
    return {
      id: this.id,
      uuid: this.uuid,
      label: this.label,
      x: this.x,
      y: this.y,
      width: this.width,
      height: this.height
    }
  }
}
