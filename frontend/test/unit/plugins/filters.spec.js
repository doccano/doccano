import { truncate } from '@/plugins/filters.js'

describe('Truncate', () => {
  test('dont do nothing', () => {
    const string = 'aiueo'
    expect(truncate(string)).toEqual(string)
  })

  test('cut the string and add clamp if string length is larger than specified length', () => {
    const string = 'aiueo'
    expect(truncate(string, 3)).toEqual('aiu...')
  })

  test('dont cut anything if string length is smaller than specified length', () => {
    const string = 'aiueo'
    expect(truncate(string, 10)).toEqual(string)
  })
})
