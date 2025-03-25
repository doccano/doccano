import { BaseRepository } from './BaseRepository'

export class SettingsRepository extends BaseRepository {
  constructor() {
    super('settings')
  }

  async fetchAll() {
    return await this.get('')
  }

  async create(params) {
    return await this.post('', params)
  }

  async clone(params) {
    return await this.post('/clone', params)
  }

  async delete(params) {
    return await this.delete('', { data: params })
  }
}