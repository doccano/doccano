import {AnnotationApplicationService} from '../annotationApplicationService'
import { LinkDTO } from '../../links/linkData'
import {SequenceLabelingDTO} from './sequenceLabelingData'
import {APISequenceLabelingRepository} from '~/repositories/tasks/sequenceLabeling/apiSequenceLabeling'
import {SequenceLabelingLabel} from '~/domain/models/tasks/sequenceLabeling'
import {LinkRepository} from "~/domain/models/links/linkRepository"
import {LinkItem} from "~/domain/models/links/link"

export class SequenceLabelingApplicationService extends AnnotationApplicationService<SequenceLabelingLabel> {
    constructor(
        readonly repository: APISequenceLabelingRepository,
        readonly linkRepository: LinkRepository
    ) {
        super(new APISequenceLabelingRepository())
    }

    public async list(projectId: string, docId: number): Promise<SequenceLabelingDTO[]> {
        const items = await this.repository.list(projectId, docId)
        return items.map(item => new SequenceLabelingDTO(item))
    }

    public async create(projectId: string, docId: number, labelId: number, startOffset: number, endOffset: number): Promise<void> {
        const item = new SequenceLabelingLabel(0, labelId, 0, startOffset, endOffset)
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

    public async listLinks(projectId: string, docId: number): Promise<LinkDTO[]> {
        const items = await this.linkRepository.list(projectId, docId)
        return items.map(item => new LinkDTO(item))
    }

    public async createLink(projectId: string, docId: number, fromId: number, toId: number, typeId: number): Promise<void> {
        const link = new LinkItem(0, fromId, toId, typeId);
        await this.linkRepository.create(projectId, docId, link);
    }

    public async deleteLink(projectId: string, docId: number, linkId: number): Promise<void> {
        await this.linkRepository.delete(projectId, docId, linkId);
    }

    public async updateLink(projectId: string, docId: number, linkId: number, linkType: number): Promise<void> {
        await this.linkRepository.update(projectId, docId, linkId, linkType);
    }
}
