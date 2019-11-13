import axios from 'axios'
const baseURL = 'http://127.0.0.1:8000/v1' // Todo: change URL by development/staging/production.

class ApiService {
  constructor() {
    this.instance = axios.create({
      baseURL
    })
  }

  setHeader(token) {
    this.instance.defaults.headers.common.Authorization = `Token ${token}`
  }

  removeHeader() {
    this.instance.defaults.headers.common = {}
  }

  request(method, url, data = {}, config = {}) {
    return this.instance({
      method,
      url,
      data,
      ...config
    })
    // .then(response => response.data)
    // .catch(error => error)
  }

  get(url, config = {}) {
    return this.request('GET', url, {}, config)
  }

  post(url, data, config = {}) {
    return this.request('POST', url, data, config)
  }

  put(url, data, config = {}) {
    return this.request('PUT', url, data, config)
  }

  patch(url, data, config = {}) {
    return this.request('PATCH', url, data, config)
  }

  delete(url, config = {}) {
    return this.request('DELETE', url, {}, config)
  }
}

export default new ApiService()
