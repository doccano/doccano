import { TagItem } from '~/domain/models/tag/tag'

export interface TagRepository {
  list(projectId: string | number): Promise<TagItem[]>

  create(projectId: string | number, item: string): Promise<TagItem>

  delete(projectId: string | number, tagId: number): Promise<void>
}
