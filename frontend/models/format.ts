import DownloadSeq2seqCSV from '@/static/formats/seq2seq/download/example.csv'
import DownloadSeq2seqJSONL from '@/static/formats/seq2seq/download/example.jsonl'
import DownloadSequenceLabelingJSONL from '@/static/formats/sequence_labeling/download/example.jsonl'
import DownloadSequenceLabelingJSONLText from '@/static/formats/sequence_labeling/download/example_text.jsonl'
import DownloadTextClassificationJSONL from '@/static/formats/text_classification/download/example.jsonl'
import DownloadTextClassificationCSV from '@/static/formats/text_classification/download/example.csv'
import DownloadTextClassificationFastText from '@/static/formats/text_classification/download/fastText.txt'
import UploadPlainText from '@/static/formats/generic/upload/example.txt'
import UploadSeq2seqCSV from '@/static/formats/seq2seq/upload/example.csv'
import UploadSeq2seqJSONL from '@/static/formats/seq2seq/upload/example.jsonl'
import UploadSequenceLabelingCoNLL from '@/static/formats/sequence_labeling/upload/example.conll.txt'
import UploadSequenceLabelingJSONL from '@/static/formats/sequence_labeling/upload/example.jsonl'
import UploadTextClassificationCSV from '@/static/formats/text_classification/upload/example.csv'
import UploadTextClassificationJSONL from '@/static/formats/text_classification/upload/example.jsonl'
import UploadTextClassificationFastText from '@/static/formats/text_classification/upload/fastText.txt'

export class FormatItem {
  constructor(
    public example: string,
    public type: string,
    public text: string,
    public extension: string
  ) {}
}

const CoNLLItem = (example: string) => { return new FormatItem(example, 'conll', 'CoNLL', 'txt') }
const CSVItem = (example: string) => { return new FormatItem(example, 'csv', 'CSV', 'csv') }
const ExcelItem = (example: string) => { return new FormatItem(example, 'excel', 'Excel', 'xlsx') }
const FastTextItem = (example: string) => { return new FormatItem(example, 'txt', 'fastText', 'txt') }
const JSONLItem = (example: string) => { return new FormatItem(example, 'json', 'JSONL', 'jsonl') }
const JSONLLabelItem = (example: string) => { return new FormatItem(example, 'json', 'JSONL(text label)', 'jsonl') }
const PlainItem = (example: string) => { return new FormatItem(example, 'plain', 'Plain text', 'txt') }

export class FormatFactory {
  constructor(private projectType: string) {}

  createDownloadFormat(): FormatItem[] {
    if (this.projectType === 'DocumentClassification') {
      return [
        CSVItem(DownloadTextClassificationCSV),
        JSONLItem(DownloadTextClassificationJSONL),
        FastTextItem(DownloadTextClassificationFastText)
      ]
    } else if (this.projectType === 'SequenceLabeling') {
      return [
        JSONLItem(DownloadSequenceLabelingJSONL),
        JSONLLabelItem(DownloadSequenceLabelingJSONLText)
      ]
    } else if (this.projectType === 'Seq2seq') {
      return [
        CSVItem(DownloadSeq2seqCSV),
        JSONLItem(DownloadSeq2seqJSONL)
      ]
    } else {
      return []
    }
  }

  createUploadFormat() {
    if (this.projectType === 'DocumentClassification') {
      return [
        PlainItem(UploadPlainText),
        CSVItem(UploadTextClassificationCSV),
        JSONLItem(UploadTextClassificationJSONL),
        ExcelItem(UploadTextClassificationCSV),
        FastTextItem(UploadTextClassificationFastText)
      ]
    } else if (this.projectType === 'SequenceLabeling') {
      return [
        PlainItem(UploadPlainText),
        JSONLItem(UploadSequenceLabelingJSONL),
        CoNLLItem(UploadSequenceLabelingCoNLL)
      ]
    } else if (this.projectType === 'Seq2seq') {
      return [
        PlainItem(UploadPlainText),
        CSVItem(UploadSeq2seqCSV),
        JSONLItem(UploadSeq2seqJSONL),
        ExcelItem(UploadSeq2seqCSV)
      ]
    } else {
      return []
    }
  }
}
