export class Catalog {
  constructor(
    public name: string,
    public accept_types: string,
    public properties: object
  ) {}

  static valueOf(
    { name, accept_types, properties }:
    { name: string, accept_types: string, properties: object }
  ): Catalog {
    return new Catalog(name, accept_types, properties)
  }
}
