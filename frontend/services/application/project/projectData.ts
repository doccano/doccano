import { ProjectReadItem, CurrentUsersRole, ProjectType } from '~/domain/models/project/project';
import { FormatItem } from '~/domain/models/document/format';


export class FormatDTO {
  example: string;
  type: string;
  text: string;
  extension: string;

  constructor(item: FormatItem) {
    this.example = item.example;
    this.type = item.type;
    this.text = item.text;
    this.extension = item.extension;
  }
}


export class ProjectDTO {
  id: number;
  name: string;
  description: string;
  guideline: string;
  current_users_role: CurrentUsersRole;
  projectType: ProjectType;
  updatedAt: string;
  enableRandomizeDocOrder: boolean;
  enableShareAnnotation: boolean;
  pageLink: string;
  downloadFormats: FormatDTO[];
  uploadFormats: FormatDTO[];
  permitApprove: Boolean;
  filterOption: String;

  constructor(item: ProjectReadItem) {
    this.id = item.id;
    this.name = item.name;
    this.description = item.description;
    this.guideline = item.guideline;
    this.current_users_role = item.current_users_role;
    this.projectType = item.project_type;
    this.updatedAt = item.updated_at;
    this.enableRandomizeDocOrder = item.randomize_document_order;
    this.enableShareAnnotation = item.collaborative_annotation;
    this.pageLink = item.annotationPageLink;
    this.downloadFormats = item.downloadFormats.map(f => new FormatDTO(f));
    this.uploadFormats = item.uploadFormats.map(f => new FormatDTO(f));
    this.permitApprove = item.permitApprove;
    this.filterOption = item.filterOption;
  }
}

export type ProjectWriteDTO = Pick<ProjectDTO, 'id' | 'name' | 'description' | 'guideline' | 'projectType' | 'enableRandomizeDocOrder' | 'enableShareAnnotation'>;
