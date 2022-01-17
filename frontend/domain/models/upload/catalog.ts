import { Expose } from 'class-transformer'

export class Catalog {
  name: string;
  example: string;
  properties: object;

  @Expose({ name: 'accept_types' })
  acceptTypes: string;
}
