import "reflect-metadata"
import { Expose, Type } from 'class-transformer'

export type ProjectType = 'DocumentClassification' | 'SequenceLabeling' | 'Seq2seq' | 'IntentDetectionAndSlotFilling' | 'ImageClassification' | 'Speech2text'


export class ProjectReadItem {
  id:                          number;
  name:                        string;
  description:                 string;
  guideline:                   string;
  users:                       number[];
  tags:                        Object[];

  @Expose({ name: 'project_type' })
  projectType: ProjectType;

  @Expose({ name: 'updated_at' })
  updatedAt: string;

  @Expose({ name: 'random_order' })
  randomOrder: boolean;

  @Expose({ name: 'collaborative_annotation' })
  collaborative_annotation: boolean;

  @Expose({ name: 'single_class_classification' })
  exclusiveCategories: boolean;

  @Expose({ name: 'resourcetype' })
  resourceType: string;

  @Expose({ name: 'allow_overlapping' })
  allowOverlapping: boolean;

  @Expose({ name: 'grapheme_mode' })
  graphemeMode: boolean;

  @Expose({ name: 'is_text_project'})
  isTextProject: boolean;

  @Expose({ name: 'can_define_label' })
  canDefineLabel: boolean;

  @Expose({ name: 'can_define_relation' })
  canDefineRelation: boolean;

  @Expose({ name: 'can_define_span'})
  canDefineSpan: boolean;

  @Expose({ name: 'can_define_category' })
  canDefineCategory: boolean;

  get annotationPageLink(): string {
    const mapping = {
      DocumentClassification: 'text-classification',
      SequenceLabeling      : 'sequence-labeling',
      Seq2seq               : 'sequence-to-sequence',
      IntentDetectionAndSlotFilling: 'intent-detection-and-slot-filling',
      ImageClassification   : 'image-classification',
      Speech2text           : 'speech-to-text',
    }
    const url = `/projects/${this.id}/${mapping[this.projectType]}`
    return url
  }

  get taskNames(): string[] {
    if (this.projectType === 'IntentDetectionAndSlotFilling') {
      return [
        'DocumentClassification',
        'SequenceLabeling',
      ]
    }
    return [this.projectType]
  }
}

export class ProjectItemList {
  count: number;
  next: string | null;
  prev: string | null;

  @Type(() => ProjectReadItem)
  @Expose({ name: 'results' })
  items: ProjectReadItem[];
}

export class ProjectWriteItem {
  constructor(
    public id:                          number,
    public name:                        string,
    public description:                 string,
    public guideline:                   string,
    public project_type:                ProjectType,
    public random_order:                boolean,
    public collaborative_annotation:    boolean,
    public single_class_classification: boolean,
    public allow_overlapping:           boolean,
    public grapheme_mode:               boolean
  ) {}

  get resourceType(): string {
    const mapping = {
      DocumentClassification: 'TextClassificationProject',
      SequenceLabeling      : 'SequenceLabelingProject',
      Seq2seq               : 'Seq2seqProject',
      IntentDetectionAndSlotFilling: 'IntentDetectionAndSlotFillingProject',
      ImageClassification   : 'ImageClassificationProject',
      Speech2text           : 'Speech2textProject',
    }
    return mapping[this.project_type]
  }

  toObject(): Object {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      guideline: this.guideline,
      project_type: this.project_type,
      random_order: this.random_order,
      collaborative_annotation: this.collaborative_annotation,
      single_class_classification: this.single_class_classification,
      allow_overlapping: this.allow_overlapping,
      grapheme_mode: this.grapheme_mode,
      resourcetype: this.resourceType
    }
  }
}
