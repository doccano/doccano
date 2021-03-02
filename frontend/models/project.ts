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
      resourcetype
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
      resourcetype:                string
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
      resourcetype
    )
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
      resourcetype: this.resourcetype
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
    public collaborative_annotation:    boolean
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
    }:
    {
      id:                          number,
      name:                        string,
      description:                 string,
      guideline:                   string,
      project_type:                ProjectType,
      randomize_document_order:    boolean,
      collaborative_annotation:    boolean
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
      resourcetype: this.resourceType
    }
  }
}
