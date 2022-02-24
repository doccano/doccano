import {LinkItem} from '~/domain/models/links/link'

export interface LinkRepository {
    list(projectId: string, exampleId: number): Promise<LinkItem[]>

    create(projectId: string, exampleId: number, link: LinkItem): Promise<LinkItem>

    update(projectId: string, exampleId: number, linkId: number, linkType: number): Promise<LinkItem>

    delete(projectId: string, exampleId: number, linkId: number): Promise<void>

    bulkDelete(projectId: string, exampleId: number, linkIds: number[]): Promise<void>
}
