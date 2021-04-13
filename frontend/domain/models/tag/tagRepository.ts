import { TagItem } from '~/domain/models/tag/tag'

export interface TagRepository {
  list(projectId: string): Promise<TagItem[]>

  create(projectId: string, item: string): Promise<TagItem>

  delete(projectId: string, tagId: number): Promise<void>
}
