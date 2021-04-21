export class Format {
  constructor(
    public name: string,
    public example: string,
    public properties: object
  ) {}

  static valueOf(
    { name, example, properties }:
    { name: string, example: string, properties: object }
  ) {
    return new Format(name, example, properties)
  }
}
