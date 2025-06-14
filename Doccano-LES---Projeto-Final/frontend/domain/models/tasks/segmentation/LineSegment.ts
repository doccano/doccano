import Flatten from '@flatten-js/core'
import Point = Flatten.Point
import Segment = Flatten.Segment

export default class LineSegment {
  readonly segment: Segment

  constructor(readonly startPoint: Point, readonly endPoint: Point) {
    this.segment = new Segment(startPoint, endPoint)
  }

  get points(): number[] {
    return [this.startPoint.x, this.startPoint.y, this.endPoint.x, this.endPoint.y]
  }

  // **
  // * Gets the closest point on the line segment to the given point.
  // * @param point The point to get the closest point to.
  // * @returns The closest point on the line segment to the given point.
  // **
  getClosestPoint(point: Point): Point {
    const [, shortestSegment] = this.segment.distanceTo(point)
    return shortestSegment.start
  }
}
