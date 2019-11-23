import CSVParser from '@/services/parsers/csv.service'

describe('Request', () => {
  const parser = new CSVParser()

  test('can parse text', () => {
    const text = 'col 1,col 2\n1,2'
    const parsed = parser.parse(text)
    expect(parsed.meta.fields).toEqual(['col 1', 'col 2'])
    expect(parsed.data[0]['col 1']).toEqual('1')
  })
})
