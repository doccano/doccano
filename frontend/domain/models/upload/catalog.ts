export class Catalog {
  constructor(
    public name: string,
    public example: string,
    public accept_types: string,
    public properties: object
  ) {}

  static valueOf(
    { name, example, accept_types, properties }:
    { name: string, example: string, accept_types: string, properties: object }
  ): Catalog {
    return new Catalog(name, example, accept_types, properties)
  }
}
