import apiService from '@/services/api.service'

export class BaseRepository {
  constructor(resource) {
    this.resource = resource
  }

  get(path, params = {}) {
    return apiService.get(`${this.resource}${path}`, { params })
      .then(response => response.data)
  }

  post(path, data = {}) {
    return apiService.post(`${this.resource}${path}`, data)
      .then(response => response.data)
  }

  put(path, data = {}) {
    return apiService.put(`${this.resource}${path}`, data)
      .then(response => response.data)
  }

  patch(path, data = {}) {
    return apiService.patch(`${this.resource}${path}`, data)
      .then(response => response.data)
  }

  delete(path, params = {}) {
    return apiService.delete(`${this.resource}${path}`, params)
      .then(response => response.data)
  }
}