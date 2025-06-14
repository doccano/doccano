import { OptionsQuestionItem, OptionsGroupItem, QuestionItem, QuestionTypeItem } from './question'

export interface QuestionRepository {
  create(projectId: string, item: QuestionItem): Promise<QuestionItem>
  list(perspectiveId: number, project_id: string): Promise<QuestionItem[]>
}

export interface OptionsGroupRepository {
  create(projectId: string, item: OptionsGroupItem): Promise<OptionsGroupItem>
  findByName(projectId: string, name: string): Promise<OptionsGroupItem>
  list(project_id: string) : Promise<OptionsGroupItem[]>
}

export interface OptionsQuestionRepository {
  create(projectId: string, item: OptionsQuestionItem): Promise<OptionsQuestionItem>
  list(projectId: string): Promise<OptionsQuestionItem[]>
}

export interface QuestionTypeRepository {
  create(projectId: string, item: QuestionTypeItem): Promise<QuestionTypeItem>
  findById(projectId: string, id: number): Promise<QuestionTypeItem>
}
