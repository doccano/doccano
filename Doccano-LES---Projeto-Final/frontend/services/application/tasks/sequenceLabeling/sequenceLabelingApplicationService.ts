import { AnnotationApplicationService } from '../annotationApplicationService'
import { RelationDTO } from './relationData'
import { SpanDTO } from './sequenceLabelingData'
import { APISpanRepository } from '@/repositories/tasks/apiSpanRepository'
import { APIRelationRepository } from '@/repositories/tasks/apiRelationRepository'
import { Span } from '@/domain/models/tasks/span'
import { Relation } from '@/domain/models/tasks/relation'

export class SequenceLabelingApplicationService extends AnnotationApplicationService<Span> {
  constructor(
    readonly repository: APISpanRepository,
    readonly relationRepository: APIRelationRepository
  ) {
    super(new APISpanRepository())
  }

  public async list(projectId: string, exampleId: number): Promise<SpanDTO[]> {
    const items = await this.repository.list(projectId, exampleId)
    return items.map((item) => new SpanDTO(item))
  }

  public async create(
    projectId: string,
    exampleId: number,
    labelId: number,
    startOffset: number,
    endOffset: number
  ): Promise<void> {
    const item = new Span(0, labelId, 0, startOffset, endOffset)
    try {
      await this.repository.create(projectId, exampleId, item)
    } catch (e: any) {
      console.log(e.response.data.detail)
    }
  }

  public async changeLabel(
    projectId: string,
    exampleId: number,
    annotationId: number,
    labelId: number
  ): Promise<void> {
    try {
      const span = await this.repository.find(projectId, exampleId, annotationId)
      span.changeLabel(labelId)
      await this.repository.update(projectId, exampleId, annotationId, span)
    } catch (e: any) {
      console.log(e.response.data.detail)
    }
  }

  public async listRelations(projectId: string, exampleId: number): Promise<RelationDTO[]> {
    const items = await this.relationRepository.list(projectId, exampleId)
    return items.map((item) => new RelationDTO(item))
  }

  public async createRelation(
    projectId: string,
    exampleId: number,
    fromId: number,
    toId: number,
    typeId: number
  ): Promise<void> {
    const relation = new Relation(0, fromId, toId, typeId)
    await this.relationRepository.create(projectId, exampleId, relation)
  }

  public async deleteRelation(
    projectId: string,
    exampleId: number,
    relationId: number
  ): Promise<void> {
    await this.relationRepository.delete(projectId, exampleId, relationId)
  }

  public async updateRelation(
    projectId: string,
    exampleId: number,
    relationId: number,
    typeId: number
  ): Promise<void> {
    const relation = await this.relationRepository.find(projectId, exampleId, relationId)
    relation.changeType(typeId)
    await this.relationRepository.update(projectId, exampleId, relationId, relation)
  }
}
