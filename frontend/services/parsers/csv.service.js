import Papa from 'papaparse'

class CSVParser {
  parse(text, options = { header: true }) {
    return Papa.parse(text, options)
  }
}

export default CSVParser
