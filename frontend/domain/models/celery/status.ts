export class Status {
  constructor(
    public ready: boolean,
    public result: object,
    public error: any
  ) {}

  static valueOf(
    { ready, result, error }:
    { ready: boolean, result: object, error: any }
  ) {
    return new Status(ready, result, error)
  }
}
