import { v4 as uuidv4 } from 'uuid'
import RectangleProps from './RectangleProps'
import LabelProps from '@/domain/models/tasks/shared/LabelProps'

export default class Rectangle {
  constructor(
    readonly label: number,
    readonly x: number,
    readonly y: number,
    readonly width: number,
    readonly height: number,
    readonly id: string = uuidv4()
  ) {}

  toProps(): RectangleProps {
    const { id, label, x, y, width, height } = this
    return { id, label, x, y, width, height }
  }

  transform(x: number, y: number, width: number, height: number): Rectangle {
    return new Rectangle(this.label, x, y, width, height, this.id)
  }

  getColor(labels: LabelProps[]): string {
    return labels.find((label) => label.id === this.label)!.color || '##ff0000'
  }

  exists(): boolean {
    return this.width !== 0 && this.height !== 0
  }

  minMaxPoints(): [number, number, number, number] {
    const minX = this.x
    const minY = this.y
    const maxX = this.x + this.width
    const maxY = this.y + this.height
    return [minX, minY, maxX, maxY]
  }
}
