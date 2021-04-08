export class Catalog {
  constructor(
    public name: string,
    public properties: object
  ) {}

  static valueOf(
    { name, properties }:
    { name: string, properties: object }
  ): Catalog {
    return new Catalog(name, properties)
  }
}
