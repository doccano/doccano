export class Page<T> {
  constructor(
    readonly count: number,
    readonly next: string | null,
    readonly prev: string | null,
    readonly items: T[]
  ) {}
}
