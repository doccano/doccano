import ApiService from '@/services/api.service'
import {LinkRepository} from "~/domain/models/links/linkRepository";
import {LinkItem} from "~/domain/models/links/link";
import {LabelItem} from "~/domain/models/label/label";
import {LabelItemResponse} from "~/repositories/label/apiLabelRepository";

export interface LinkResponse {
    id: number
    annotation_id_1: number
    annotation_id_2: number
    type: number,
    user: number,
    timestamp: string
}

export class ApiLinkRepository implements LinkRepository {
    constructor(
        private readonly request = ApiService
    ) {
    }

    async list(projectId: string): Promise<LinkItem[]> {
        const url = `/projects/${projectId}/annotation_relations`
        const response = await this.request.get(url)
        const responseLinks: LinkResponse[] = response.data
        return responseLinks.map(link => LinkItem.valueOf(link))
    }

    async create(projectId: string, item: LinkItem): Promise<LinkItem> {
        const url = `/projects/${projectId}/annotation_relations`
        const response = await this.request.post(url, item.toObject())
        const responseItem: LinkResponse = response.data
        return LinkItem.valueOf(responseItem)
    }

    async update(projectId: string, linkId: number, linkType: number): Promise<LinkItem> {
        const url = `/projects/${projectId}/annotation_relations/${linkId}`
        const response = await this.request.patch(url, {type: linkType})
        const responseItem: LinkResponse = response.data
        return LinkItem.valueOf(responseItem)
    }

    async bulkDelete(projectId: string, linkIds: number[]): Promise<void> {
        const url = `/projects/${projectId}/annotation_relations`
        await this.request.delete(url, {ids: linkIds})
    }
}
