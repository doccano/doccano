export interface CurrentUsersRole {
  is_project_admin:       boolean;
  is_annotator:           boolean;
  is_annotation_approver: boolean;
}

export type ProjectType = 'DocumentClassification' | 'SequenceLabeling' | 'Seq2seq' | 'IntentDetectionAndSlotFilling' | 'ImageClassification' | 'Speech2text'


export class ProjectReadItem {
  constructor(
    public id:                          number,
    public name:                        string,
    public description:                 string,
    public guideline:                   string,
    public users:                       number[],
    public current_users_role:          CurrentUsersRole,
    public project_type:                ProjectType,
    public updated_at:                  string,
    public random_order:                boolean,
    public collaborative_annotation:    boolean,
    public single_class_classification: boolean,
    public resourcetype:                string,
    public allow_overlapping:           boolean,
    public grapheme_mode:               boolean,
    public tags:                        Object[],
  ) {}

  static valueOf(
    {
      id,
      name,
      description,
      guideline,
      users,
      current_users_role,
      project_type,
      updated_at,
      random_order,
      collaborative_annotation,
      single_class_classification,
      resourcetype,
      allow_overlapping,
      grapheme_mode,
      tags
    }:
    {
      id:                          number,
      name:                        string,
      description:                 string,
      guideline:                   string,
      users:                       number[],
      current_users_role:          CurrentUsersRole,
      project_type:                ProjectType,
      updated_at:                  string,
      random_order:                boolean,
      collaborative_annotation:    boolean,
      single_class_classification: boolean,
      resourcetype:                string,
      allow_overlapping:           boolean,
      grapheme_mode:               boolean,
      tags:                        Object[]
    }
  ): ProjectReadItem {
    return new ProjectReadItem(
      id,
      name,
      description,
      guideline,
      users,
      current_users_role,
      project_type,
      updated_at,
      random_order,
      collaborative_annotation,
      single_class_classification,
      resourcetype,
      allow_overlapping,
      grapheme_mode,
      tags
    )
  }

  get annotationPageLink(): string {
    const mapping = {
      DocumentClassification: 'text-classification',
      SequenceLabeling      : 'sequence-labeling',
      Seq2seq               : 'sequence-to-sequence',
      IntentDetectionAndSlotFilling: 'intent-detection-and-slot-filling',
      ImageClassification   : 'image-classification',
      Speech2text           : 'speech-to-text',
    }
    const url = `/projects/${this.id}/${mapping[this.project_type]}`
    return url
  }

  get canDefineLabel() {
    const allowedProjectTypes = [
      'DocumentClassification',
      'SequenceLabeling',
      'IntentDetectionAndSlotFilling',
      'ImageClassification'
    ]
    return allowedProjectTypes.includes(this.project_type)
  }

  get canDefineRelation() {
    const allowedProjectTypes = [
      'SequenceLabeling'
    ]
    return allowedProjectTypes.includes(this.project_type)
  }

  get isTextProject() {
    const allowedProjectTypes = [
      'DocumentClassification',
      'SequenceLabeling',
      'Seq2seq',
      'IntentDetectionAndSlotFilling'
    ]
    return allowedProjectTypes.includes(this.project_type)
  }

  get hasCategory(): boolean {
    const allowedProjectTypes = [
      'DocumentClassification',
      'IntentDetectionAndSlotFilling',
      'ImageClassification'
    ]
    return allowedProjectTypes.includes(this.project_type)
  }

  get hasSpan(): boolean {
    const allowedProjectTypes = [
      'IntentDetectionAndSlotFilling',
      'SequenceLabeling'
    ]
    return allowedProjectTypes.includes(this.project_type)
  }

  toObject(): Object {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      guideline: this.guideline,
      users: this.users,
      current_users_role: this.current_users_role,
      project_type: this.project_type,
      updated_at: this.updated_at,
      random_order: this.random_order,
      collaborative_annotation: this.collaborative_annotation,
      single_class_classification: this.single_class_classification,
      resourcetype: this.resourcetype,
      allow_overlapping: this.allow_overlapping,
      grapheme_mode: this.grapheme_mode,
      tags: this.tags
    }
  }
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

  static valueOf(
    {
      id,
      name,
      description,
      guideline,
      project_type,
      random_order,
      collaborative_annotation,
      single_class_classification,
      allow_overlapping,
      grapheme_mode
    }:
    {
      id:                          number,
      name:                        string,
      description:                 string,
      guideline:                   string,
      project_type:                ProjectType,
      random_order:                boolean,
      collaborative_annotation:    boolean,
      single_class_classification: boolean,
      allow_overlapping:           boolean,
      grapheme_mode:               boolean
    }
  ): ProjectWriteItem {
    return new ProjectWriteItem(
      id,
      name,
      description,
      guideline,
      project_type,
      random_order,
      collaborative_annotation,
      single_class_classification,
      allow_overlapping,
      grapheme_mode
    )
  }

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
