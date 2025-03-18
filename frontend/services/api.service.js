import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

class ApiService {
  constructor() {
    this.instance = axios.create({
      baseURL: process.env.baseUrl,
      withCredentials: true
    })
  }

  request(method, url, data = {}, config = {}) {
    return this.instance({
      method,
      url,
      data,
      ...config
    })
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

  delete(url, data = {}, config = {}) {
    return this.request('DELETE', url, data, config)
  }
}

export default new ApiService()
