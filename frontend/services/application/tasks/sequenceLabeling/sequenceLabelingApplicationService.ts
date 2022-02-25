import { AnnotationApplicationService } from '../annotationApplicationService'
import { RelationDTO } from './relationData'
import { SpanDTO } from './sequenceLabelingData'
import { APISequenceLabelingRepository } from '~/repositories/tasks/sequenceLabeling/apiSequenceLabeling'
import { Span } from '~/domain/models/tasks/sequenceLabeling'
import { RelationRepository } from "~/domain/models/tasks/relationRepository"
import { RelationItem } from "~/domain/models/tasks/relation"

export class SequenceLabelingApplicationService extends AnnotationApplicationService<Span> {
    constructor(
        readonly repository: APISequenceLabelingRepository,
        readonly relationRepository: RelationRepository
    ) {
        super(new APISequenceLabelingRepository())
    }

    public async list(projectId: string, docId: number): Promise<SpanDTO[]> {
        const items = await this.repository.list(projectId, docId)
        return items.map(item => new SpanDTO(item))
    }

    public async create(projectId: string, docId: number, labelId: number, startOffset: number, endOffset: number): Promise<void> {
        const item = new Span(0, labelId, 0, startOffset, endOffset)
        try {
            await this.repository.create(projectId, docId, item)
        } catch(e: any) {
            console.log(e.response.data.detail)
        }
    }

    public async changeLabel(projectId: string, docId: number, annotationId: number, labelId: number): Promise<void> {
        try {
            await this.repository.update(projectId, docId, annotationId, labelId)
        } catch(e: any) {
            console.log(e.response.data.detail)
        }
    }

    public async listRelations(projectId: string, docId: number): Promise<RelationDTO[]> {
        const items = await this.relationRepository.list(projectId, docId)
        return items.map(item => new RelationDTO(item))
    }

    public async createRelation(projectId: string, docId: number, fromId: number, toId: number, typeId: number): Promise<void> {
        const relation = new RelationItem(0, fromId, toId, typeId)
        await this.relationRepository.create(projectId, docId, relation)
    }

    public async deleteRelation(projectId: string, docId: number, relationId: number): Promise<void> {
        await this.relationRepository.delete(projectId, docId, relationId)
    }

    public async updateRelation(projectId: string, docId: number, relationId: number, typeId: number): Promise<void> {
        await this.relationRepository.update(projectId, docId, relationId, typeId)
    }
}
