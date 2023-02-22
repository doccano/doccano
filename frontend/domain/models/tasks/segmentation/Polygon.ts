import { v4 as uuidv4 } from 'uuid'
import Flatten from '@flatten-js/core'
import LineSegment from './LineSegment'
import PolygonProps from './PolygonProps'
import ValidationError from './errors'
import LabelProps from '@/domain/models/tasks/shared/LabelProps'
import Point = Flatten.Point
import Vector = Flatten.Vector

const MINIMUM_NUMBER_OF_SIDES = 3

export default class Polygon {
  readonly id: string

  readonly labelId: number

  points: Point[] = []

  constructor(labelId: number, points: number[] = [], id: string = uuidv4()) {
    if (points.length % 2 !== 0) {
      throw new ValidationError('Invalid number of points')
    }
    this.id = id
    this.labelId = labelId
    for (let i = 0; i < points.length; i += 2) {
      this.addPoint(points[i], points[i + 1])
    }
  }

  clone(): Polygon {
    return new Polygon(this.labelId, this.flattenedPoints, this.id)
  }

  translate(x: number, y: number): void {
    const vector = new Vector(x, y)
    this.points = this.points.map((point) => point.translate(vector))
  }

  canBeClosed(): boolean {
    return this.points.length >= MINIMUM_NUMBER_OF_SIDES
  }

  addPoint(x: number, y: number): void {
    const point = new Point(x, y)
    this.points.push(point)
  }

  movePoint(index: number, x: number, y: number): void {
    const point = new Point(x, y)
    this.points[index] = point
  }

  removePoint(index: number): void {
    if (this.points.length > MINIMUM_NUMBER_OF_SIDES) {
      this.points.splice(index, 1)
    }
  }

  insertPoint(x: number, y: number, index: number): void {
    const point = new Point(x, y)
    this.points.splice(index, 0, point)
  }

  toPoints(): Point[] {
    return this.points.map((point) => point.clone())
  }

  minMaxPoints(): [number, number, number, number] {
    const [minX, minY, maxX, maxY] = this.points.reduce(
      ([minx, miny, maxx, maxy], point) => [
        Math.min(minx, point.x),
        Math.min(miny, point.y),
        Math.max(maxx, point.x),
        Math.max(maxy, point.y)
      ],
      [Infinity, Infinity, -Infinity, -Infinity]
    )
    return [minX, minY, maxX, maxY]
  }

  toProps(): PolygonProps {
    return {
      id: this.id,
      label: this.labelId,
      points: this.points.flatMap((point) => [point.x, point.y])
    }
  }

  getColor(labels: LabelProps[]): string {
    return labels.find((label) => label.id === this.labelId)!.color || '##ff0000'
  }

  get lineSegments(): LineSegment[] {
    const lineSegments = []
    for (let i = 0; i < this.points.length; i += 1) {
      const p1 = this.points[i]
      const p2 = this.points[(i + 1) % this.points.length]
      lineSegments.push(new LineSegment(p1, p2))
    }
    return lineSegments
  }

  get flattenedPoints(): number[] {
    return this.points.flatMap((point) => [point.x, point.y])
  }

  get numberOfSides(): number {
    return this.points.length
  }
}
