export class Scaler {
  private u = 0

  private s = 1

  fit(u: number, s: number): void {
    this.u = u
    this.s = s
  }

  transform(value: number): number {
    return (value - this.u) / this.s
  }

  inverse(value: number): number {
    return value * this.s + this.u
  }
}

export const transform = (value: number, u: number, s: number): number => (value - u) / s

export const inverseTransform = (value: number, u: number, s: number): number => value * s + u
