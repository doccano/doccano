import MockAdapter from 'axios-mock-adapter'
import ApiService from '@/services/api.service'

describe('Request', () => {
  const r = new ApiService('')
  const mockAxios = new MockAdapter(r.instance)

  test('can get resources', async () => {
    const data = [
      {
        id: 1,
        title: 'title',
        body: 'body'
      }
    ]
    mockAxios.onGet('/posts').reply(200, data)
    const response = await r.get('/posts')
    expect(response).toEqual(data)
  })

  test('can create a resource', async () => {
    const data = {
      title: 'foo',
      body: 'bar'
    }
    mockAxios.onPost('/posts').reply(201, data)
    const response = await r.post('/posts', data)
    expect(response.title).toEqual(data.title)
  })

  test('can update a resource', async () => {
    const data = {
      id: 1,
      title: 'foo',
      body: 'bar'
    }
    mockAxios.onPut('/posts/1').reply(204, data)
    const response = await r.put('/posts/1', data)
    expect(response.title).toEqual(data.title)
  })

  test('can partially update a resource', async () => {
    const data = {
      title: 'foo'
    }
    mockAxios.onPatch('/posts/1').reply(200, data)
    const response = await r.patch('/posts/1', data)
    expect(response.title).toEqual(data.title)
  })

  test('can delete a resource', async () => {
    mockAxios.onDelete('/posts/1').reply(204, {})
    const response = await r.delete('/posts/1')
    expect(response).toEqual({})
  })
})
