import {LinkItem} from '~/domain/models/links/link'

export interface LinkRepository {
    create(projectId: string, link: LinkItem): Promise<LinkItem>

    update(projectId: string, linkId: number, linkType: number): Promise<LinkItem>

    bulkDelete(projectId: string, linkIds: number[]): Promise<void>
}
