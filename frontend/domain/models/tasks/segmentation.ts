export class SegmentationItem {
  constructor(
    public id: number,
    public uuid: string,
    public label: number,
    public points: number[]
  ) {}

  static valueOf({
    id,
    uuid,
    label,
    points
  }: {
    id: number
    uuid: string
    label: number
    points: number[]
  }): SegmentationItem {
    return new SegmentationItem(id, uuid, label, points)
  }

  toObject(): Object {
    return {
      id: this.id,
      uuid: this.uuid,
      label: this.label,
      points: this.points
    }
  }
}
