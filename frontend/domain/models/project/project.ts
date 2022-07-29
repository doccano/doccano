export type ProjectType =
  | 'DocumentClassification'
  | 'SequenceLabeling'
  | 'Seq2seq'
  | 'IntentDetectionAndSlotFilling'
  | 'ImageClassification'
  | 'ImageCaptioning'
  | 'BoundingBox'
  | 'Segmentation'
  | 'Speech2text'

export class ProjectReadItem {
  constructor(
    readonly id: number,
    readonly name: string,
    readonly description: string,
    readonly guideline: string,
    readonly users: number[],
    readonly tags: Object[],
    readonly projectType: ProjectType,
    readonly updatedAt: string,
    readonly randomOrder: boolean,
    readonly collaborativeAnnotation: boolean,
    readonly exclusiveCategories: boolean,
    readonly resourceType: string,
    readonly allowOverlapping: boolean,
    readonly graphemeMode: boolean,
    readonly useRelation: boolean,
    readonly isTextProject: boolean,
    readonly canDefineLabel: boolean,
    readonly canDefineRelation: boolean,
    readonly canDefineSpan: boolean,
    readonly canDefineCategory: boolean
  ) {}

  get annotationPageLink(): string {
    const mapping = {
      DocumentClassification: 'text-classification',
      SequenceLabeling: 'sequence-labeling',
      Seq2seq: 'sequence-to-sequence',
      IntentDetectionAndSlotFilling: 'intent-detection-and-slot-filling',
      ImageClassification: 'image-classification',
      ImageCaptioning: 'image-captioning',
      BoundingBox: 'object-detection',
      Segmentation: 'segmentation',
      Speech2text: 'speech-to-text'
    }
    const url = `/projects/${this.id}/${mapping[this.projectType]}`
    return url
  }

  get taskNames(): string[] {
    if (this.projectType === 'IntentDetectionAndSlotFilling') {
      return ['DocumentClassification', 'SequenceLabeling']
    }
    return [this.projectType]
  }
}

export class ProjectItemList {
  constructor(
    readonly count: number,
    readonly next: string | null,
    readonly prev: string | null,
    readonly items: ProjectReadItem[]
  ) {}
}

export class ProjectWriteItem {
  constructor(
    public id: number,
    public name: string,
    public description: string,
    public guideline: string,
    public projectType: ProjectType,
    public randomOrder: boolean,
    public collaborativeAnnotation: boolean,
    public exclusiveCategories: boolean,
    public allowOverlapping: boolean,
    public graphemeMode: boolean,
    public useRelation: boolean,
    public tags: string[]
  ) {}

  get resourceType(): string {
    const mapping = {
      DocumentClassification: 'TextClassificationProject',
      SequenceLabeling: 'SequenceLabelingProject',
      Seq2seq: 'Seq2seqProject',
      IntentDetectionAndSlotFilling: 'IntentDetectionAndSlotFillingProject',
      ImageClassification: 'ImageClassificationProject',
      ImageCaptioning: 'ImageCaptioningProject',
      BoundingBox: 'BoundingBoxProject',
      Segmentation: 'SegmentationProject',
      Speech2text: 'Speech2textProject'
    }
    return mapping[this.projectType]
  }
}
