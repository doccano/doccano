export const DocumentClassification = 'DocumentClassification'
export const SequenceLabeling = 'SequenceLabeling'
export const Seq2seq = 'Seq2seq'
export const IntentDetectionAndSlotFilling = 'IntentDetectionAndSlotFilling'
export const ImageClassification = 'ImageClassification'
export const ImageCaptioning = 'ImageCaptioning'
export const BoundingBox = 'BoundingBox'
export const Segmentation = 'Segmentation'
export const Speech2text = 'Speech2text'

export const allProjectTypes = <const>[
  DocumentClassification,
  SequenceLabeling,
  Seq2seq,
  IntentDetectionAndSlotFilling,
  ImageClassification,
  ImageCaptioning,
  BoundingBox,
  Segmentation,
  Speech2text
]
export type ProjectType = typeof allProjectTypes[number]

export class Project {
  projectType: ProjectType
  constructor(
    readonly id: number,
    readonly name: string,
    readonly description: string,
    readonly guideline: string,
    readonly _projectType: string,
    readonly randomOrder: boolean,
    readonly enableSharingMode: boolean,
    readonly exclusiveCategories: boolean,
    readonly allowOverlappingSpans: boolean,
    readonly enableGraphemeMode: boolean,
    readonly useRelation: boolean,
    readonly tags: Object[],
    readonly users: number[] = [],
    readonly createdAt: string = '',
    readonly updatedAt: string = '',
    readonly author: string = '',
    readonly isTextProject: boolean = false
  ) {
    if (!allProjectTypes.includes(_projectType as ProjectType)) {
      throw new Error(`Invalid project type: ${_projectType}`)
    }
    this.projectType = _projectType as ProjectType
  }

  static create(
    id: number,
    name: string,
    description: string,
    guideline: string,
    projectType: string,
    randomOrder: boolean,
    enableSharingMode: boolean,
    exclusiveCategories: boolean,
    allowOverlappingSpans: boolean,
    enableGraphemeMode: boolean,
    useRelation: boolean,
    tags: Object[]
  ) {
    return new Project(
      id,
      name,
      description,
      guideline,
      projectType,
      randomOrder,
      enableSharingMode,
      exclusiveCategories,
      allowOverlappingSpans,
      enableGraphemeMode,
      useRelation,
      tags
    )
  }

  get canDefineLabel(): boolean {
    return this.canDefineCategory || this.canDefineSpan
  }

  get canDefineCategory(): boolean {
    return [
      DocumentClassification,
      IntentDetectionAndSlotFilling,
      ImageClassification,
      BoundingBox,
      Segmentation
    ].includes(this.projectType)
  }

  get canDefineSpan(): boolean {
    return [SequenceLabeling, IntentDetectionAndSlotFilling].includes(this.projectType)
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
    if (this.projectType === DocumentClassification) {
      return 'TextClassificationProject'
    }
    return `${this.projectType}Project`
  }
}
