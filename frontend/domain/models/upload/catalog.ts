import { Expose } from 'class-transformer'

export class Catalog {
  name: string
  example: string
  properties: object

  @Expose({ name: 'task_id' })
  taskId: string

  @Expose({ name: 'display_name' })
  displayName: string

  @Expose({ name: 'accept_types' })
  acceptTypes: string
}
