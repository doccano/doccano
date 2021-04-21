export interface CurrentUsersRole {
  is_project_admin:       boolean;
  is_annotator:           boolean;
  is_annotation_approver: boolean;
}

export type ProjectType = 'DocumentClassification' | 'SequenceLabeling' | 'Seq2seq'


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
    public randomize_document_order:    boolean,
    public collaborative_annotation:    boolean,
    public single_class_classification: boolean,
    public resourcetype:                string,
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
      randomize_document_order,
      collaborative_annotation,
      single_class_classification,
      resourcetype,
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
      randomize_document_order:    boolean,
      collaborative_annotation:    boolean,
      single_class_classification: boolean,
      resourcetype:                string,
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
      randomize_document_order,
      collaborative_annotation,
      single_class_classification,
      resourcetype,
      tags
    )
  }

  get annotationPageLink(): string {
    const mapping = {
      DocumentClassification: 'text-classification',
      SequenceLabeling      : 'sequence-labeling',
      Seq2seq               : 'sequence-to-sequence'
    }
    const url = `/projects/${this.id}/${mapping[this.project_type]}`
    return url
  }

  get permitApprove(): Boolean {
    const role = this.current_users_role
    return role && !role.is_annotator
  }

  get filterOption() {
    if (this.project_type === 'DocumentClassification') {
      return 'doc_annotations__isnull'
    } else if (this.project_type === 'SequenceLabeling') {
      return 'seq_annotations__isnull'
    } else if (this.project_type === 'Seq2seq') {
      return 'seq2seq_annotations__isnull'
    } else {
      return ''
    }
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
      randomize_document_order: this.randomize_document_order,
      collaborative_annotation: this.collaborative_annotation,
      single_class_classification: this.single_class_classification,
      resourcetype: this.resourcetype,
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
    public randomize_document_order:    boolean,
    public collaborative_annotation:    boolean,
    public single_class_classification: boolean
  ) {}

  static valueOf(
    {
      id,
      name,
      description,
      guideline,
      project_type,
      randomize_document_order,
      collaborative_annotation,
      single_class_classification
    }:
    {
      id:                          number,
      name:                        string,
      description:                 string,
      guideline:                   string,
      project_type:                ProjectType,
      randomize_document_order:    boolean,
      collaborative_annotation:    boolean,
      single_class_classification: boolean
    }
  ): ProjectWriteItem {
    return new ProjectWriteItem(
      id,
      name,
      description,
      guideline,
      project_type,
      randomize_document_order,
      collaborative_annotation,
      single_class_classification
    )
  }

  get resourceType(): string {
    const mapping = {
      DocumentClassification: 'TextClassificationProject',
      SequenceLabeling      : 'SequenceLabelingProject',
      Seq2seq               : 'Seq2seqProject'
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
      randomize_document_order: this.randomize_document_order,
      collaborative_annotation: this.collaborative_annotation,
      single_class_classification: this.single_class_classification,
      resourcetype: this.resourceType
    }
  }
}
