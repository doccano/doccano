import { SequenceLabelingLabel } from '~/domain/models/tasks/sequenceLabeling'


export class SequenceLabelingDTO {
  id: number;
  label: number;
  user: number;
  startOffset: number;
  endOffset: number;

  constructor(item: SequenceLabelingLabel) {
    this.id = item.id;
    this.label = item.label;
    this.user = item.user;
    this.startOffset = item.startOffset;
    this.endOffset = item.endOffset;
  }
}
