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
    readonly projectType: ProjectType,
    readonly randomOrder: boolean,
    readonly collaborativeAnnotation: boolean,
    readonly exclusiveCategories: boolean,
    readonly allowOverlapping: boolean,
    readonly graphemeMode: boolean,
    readonly useRelation: boolean,
    readonly tags: Object[],
    readonly users: number[] = [],
    readonly createdAt: string = '',
    readonly updatedAt: string = '',
    readonly author: string = '',
    readonly isTextProject: boolean = false
  ) {}

  static create(
    id: number,
    name: string,
    description: string,
    guideline: string,
    projectType: ProjectType,
    randomOrder: boolean,
    collaborativeAnnotation: boolean,
    exclusiveCategories: boolean,
    allowOverlapping: boolean,
    graphemeMode: boolean,
    useRelation: boolean,
    tags: Object[]
  ) {
    return new ProjectReadItem(
      id,
      name,
      description,
      guideline,
      projectType,
      randomOrder,
      collaborativeAnnotation,
      exclusiveCategories,
      allowOverlapping,
      graphemeMode,
      useRelation,
      tags
    )
  }

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
