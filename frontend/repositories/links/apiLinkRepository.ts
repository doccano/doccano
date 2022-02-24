import ApiService from '@/services/api.service'
import {LinkRepository} from "~/domain/models/links/linkRepository";
import {LinkItem} from "~/domain/models/links/link";

export class ApiLinkRepository implements LinkRepository {
    constructor(
        private readonly request = ApiService
    ) {
    }

    async list(projectId: string, exampleId: number): Promise<LinkItem[]> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations`
        const response = await this.request.get(url)
        return response.data.map((link: any) => LinkItem.valueOf(link))
    }

    async create(projectId: string, exampleId: number, item: LinkItem): Promise<LinkItem> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations`
        const response = await this.request.post(url, item.toObject())
        return LinkItem.valueOf(response.data)
    }

    async update(projectId: string, exampleId: number, linkId: number, linkType: number): Promise<LinkItem> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations/${linkId}`
        const response = await this.request.patch(url, {type: linkType})
        return LinkItem.valueOf(response.data)
    }

    async delete(projectId: string, exampleId: number, linkId: number): Promise<void> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations/${linkId}`
        const response = await this.request.delete(url)
    }

    async bulkDelete(projectId: string, exampleId: number, linkIds: number[]): Promise<void> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations`
        await this.request.delete(url, {ids: linkIds})
    }
}
