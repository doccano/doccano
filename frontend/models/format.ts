import Seq2seqCSV from '@/static/formats/seq2seq/download/example.csv'
import Seq2seqJSONL from '@/static/formats/seq2seq/download/example.jsonl'
import SequenceLabelingJSONL from '@/static/formats/sequence_labeling/download/example.jsonl'
import SequenceLabelingJSONLText from '@/static/formats/sequence_labeling/download/example_text.jsonl'
import TextClassificationJSONL from '@/static/formats/text_classification/download/example.jsonl'
import TextClassificationCSV from '@/static/formats/text_classification/download/example.csv'
import TextClassificationFastText from '@/static/formats/text_classification/download/fastText.txt'

export class FormatItem {
  constructor(
    public example: string,
    public type: string,
    public text: string,
    public extension: string
  ) {}
}

const CSVItem = (example: string) => { return new FormatItem(example, 'csv', 'CSV', 'csv') }

const JSONLItem = (example: string) => { return new FormatItem(example, 'json', 'JSONL', 'jsonl') }

const JSONLLabelItem = (example: string) => { return new FormatItem(example, 'json', 'JSONL(text label)', 'jsonl') }

const FastTextItem = (example: string) => { return new FormatItem(example, 'txt', 'fastText', 'txt') }


export class FormatFactory {
  constructor(private projectType: string) {}

  createDownloadFormat(): FormatItem[] {
    if (this.projectType === 'DocumentClassification') {
      return [
        CSVItem(TextClassificationCSV),
        JSONLItem(TextClassificationJSONL),
        FastTextItem(TextClassificationFastText)
      ]
    } else if (this.projectType === 'SequenceLabeling') {
      return [
        JSONLItem(SequenceLabelingJSONL),
        JSONLLabelItem(SequenceLabelingJSONLText)
      ]
    } else if (this.projectType === 'Seq2seq') {
      return [
        CSVItem(Seq2seqCSV),
        JSONLItem(Seq2seqJSONL)
      ]
    } else {
      return []
    }
  }
}
