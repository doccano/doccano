import { LinkItem } from '~/domain/models/links/link'

export interface LinksRepository {
  list(projectId: string): Promise<LinkItem[]>

  create(projectId: string, item: LinkItem): Promise<LinkItem>

  update(projectId: string, item: LinkItem): Promise<LinkItem>

  bulkDelete(projectId: string, linkIds: number[]): Promise<void>
}
