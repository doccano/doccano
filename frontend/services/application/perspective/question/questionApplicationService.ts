import {
  CreateOptionsGroupCommand,
  CreateOptionsQuestionCommand,
  CreateQuestionCommand
} from './questionCommand'
import { OptionsGroupDTO, OptionsQuestionDTO, QuestionDTO, QuestionTypeDTO } from './questionData'
import { AnswerItem } from '~/domain/models/perspective/answer/answer'
import {
  OptionsGroupItem,
  OptionsQuestionItem,
  QuestionItem,
  QuestionTypeItem
} from '~/domain/models/perspective/question/question'
import {
  OptionsGroupRepository,
  OptionsQuestionRepository,
  QuestionRepository,
  QuestionTypeRepository
} from '~/domain/models/perspective/question/questionRepository'

export class QuestionApplicationService {
  constructor(private readonly repository: QuestionRepository) {}

  public async create(item: CreateQuestionCommand): Promise<QuestionDTO> {
    const answers = item.answers.map((a) => new AnswerItem(0, a.answer, a.memberId, a.questionId))
    const question = new QuestionItem(
      0,
      item.question,
      item.type,
      answers,
      item.perspective_id,
      item.options_group
    )

    const created = await this.repository.create(question)
    return new QuestionDTO(created)
  }

  public async list(): Promise<QuestionDTO[]> {
    const questions = await this.repository.list()
    return questions.map((question) => new QuestionDTO(question))
  }
}
export class OptionsGroupApplicationService {
  constructor(private readonly repository: OptionsGroupRepository) {}

  public async create(
    project_id: string,
    item: CreateOptionsGroupCommand
  ): Promise<OptionsGroupDTO> {
    const optionsGroup = new OptionsGroupItem(0, item.name, item.options_questions)

    const created = await this.repository.create(project_id, optionsGroup)
    return new OptionsGroupDTO(created)
  }

  public async findByName(projectId: string, name: string): Promise<OptionsGroupDTO> {
    const item = await this.repository.findByName(projectId, name)
    return new OptionsGroupDTO(item)
  }
}

export class OptionsQuestionApplicationService {
  constructor(private readonly repository: OptionsQuestionRepository) {}

  public async create(
    project_id: string,
    item: CreateOptionsQuestionCommand
  ): Promise<OptionsQuestionDTO> {
    const optionsQuestion = new OptionsQuestionItem(0, item.option, 0)

    const created = await this.repository.create(project_id, optionsQuestion)
    return new OptionsQuestionDTO(created)
  }
}

export class QuestionTypeApplicationService {
  constructor(private readonly repository: QuestionTypeRepository) {}

  public async create(project_id: string, item: QuestionTypeDTO): Promise<QuestionTypeDTO> {
    const questionType = new QuestionTypeItem(item.id, item.question_type)

    const created = await this.repository.create(project_id, questionType)
    return new QuestionTypeDTO(created)
  }

  public async findById(projectId: string, id: number): Promise<QuestionTypeDTO> {
    const item = await this.repository.findById(projectId, id)
    return new QuestionTypeDTO(item)
  }
}
