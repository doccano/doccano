import { QuestionItem } from './question/question'

export class PerspectiveItem {
  constructor(
    readonly id: number,
    readonly project_id: number,
    readonly questions: QuestionItem[],
    readonly members: number[]
  ) {}

  static create(project_id: number, questions: QuestionItem[], members: number[]): PerspectiveItem {
    return new PerspectiveItem(0, project_id, questions, members)
  }

  /*
  static list(items: { id: number; project_id: number; questions: any[]; members: number[] }[]): PerspectiveItem[] {
    return items.map(item => new PerspectiveItem(
      item.id,
      item.project_id,
      QuestionItem.list(item.questions),
      item.members
    ));
  }
    */
}
