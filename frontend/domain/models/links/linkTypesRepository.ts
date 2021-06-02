import { LinkTypeItem } from '~/domain/models/links/link'

export interface LinkTypesRepository {
  list(projectId: string): Promise<LinkTypeItem[]>

  create(projectId: string, item: LinkTypeItem): Promise<LinkTypeItem>

  update(projectId: string, item: LinkTypeItem): Promise<LinkTypeItem>

  bulkDelete(projectId: string, linkIds: number[]): Promise<void>
}
