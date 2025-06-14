export class StepCounter {
  private step: number

  constructor(private readonly minStep: number = 1, private readonly maxStep: number = 10) {
    this.step = 1
  }

  static valueOf(minStep: number = 1, maxStep: number = 10): StepCounter {
    return new StepCounter(minStep, maxStep)
  }

  get count(): number {
    return this.step
  }

  set count(val: number) {
    this.step = val
  }

  next(): void {
    this.step = Math.min(this.step + 1, this.maxStep)
  }

  prev(): void {
    this.step = Math.max(this.step - 1, this.minStep)
  }

  first(): void {
    this.step = this.minStep
  }

  last(): void {
    this.step = this.maxStep
  }

  hasNext(): boolean {
    return this.step !== this.maxStep
  }

  hasPrev(): boolean {
    return this.step !== this.minStep
  }

  isFirst(): boolean {
    return this.step === this.minStep
  }

  isLast(): boolean {
    return this.step === this.maxStep
  }
}
