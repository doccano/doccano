import { Status } from '@/domain/models/celery/status'

export class StatusDTO {
  ready: boolean
  result: object
  error: any

  constructor(item: Status) {
    this.ready = item.ready
    this.result = item.result
    this.error = item.error
  }
}
