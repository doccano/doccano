const DocumentClassification = 'DocumentClassification'
const SequenceLabeling = 'SequenceLabeling'
const Seq2seq = 'Seq2seq'
const IntentDetectionAndSlotFilling = 'IntentDetectionAndSlotFilling'
const ImageClassification = 'ImageClassification'
const ImageCaptioning = 'ImageCaptioning'
const BoundingBox = 'BoundingBox'
const Segmentation = 'Segmentation'
const Speech2text = 'Speech2text'

export type ProjectType =
  | typeof DocumentClassification
  | typeof SequenceLabeling
  | typeof Seq2seq
  | typeof IntentDetectionAndSlotFilling
  | typeof ImageClassification
  | typeof ImageCaptioning
  | typeof BoundingBox
  | typeof Segmentation
  | typeof Speech2text

export class ProjectReadItem {
  constructor(
    readonly id: number,
    readonly name: string,
    readonly description: string,
    readonly guideline: string,
    readonly users: number[],
    readonly tags: Object[],
    readonly projectType: ProjectType,
    readonly createdAt: string,
    readonly updatedAt: string,
    readonly author: string,
    readonly randomOrder: boolean,
    readonly collaborativeAnnotation: boolean,
    readonly exclusiveCategories: boolean,
    readonly resourceType: string,
    readonly allowOverlapping: boolean,
    readonly graphemeMode: boolean,
    readonly useRelation: boolean,
    readonly isTextProject: boolean
  ) {}

  get canDefineLabel(): boolean {
    return this.canDefineCategory || this.canDefineSpan
  }

  get canDefineCategory(): boolean {
    return (
      this.projectType in
      [
        DocumentClassification,
        IntentDetectionAndSlotFilling,
        ImageClassification,
        BoundingBox,
        Segmentation
      ]
    )
  }

  get canDefineSpan(): boolean {
    return this.projectType in [SequenceLabeling, IntentDetectionAndSlotFilling]
  }

  get canDefineRelation(): boolean {
    return this.useRelation
  }

  get taskNames(): string[] {
    if (this.projectType === IntentDetectionAndSlotFilling) {
      return [DocumentClassification, SequenceLabeling]
    }
    return [this.projectType]
  }
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
