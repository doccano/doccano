export class Category {
  constructor(readonly id: number, readonly label: number, readonly user: number) {}

  public static create(label: number): Category {
    return new Category(0, label, 0)
  }
}
