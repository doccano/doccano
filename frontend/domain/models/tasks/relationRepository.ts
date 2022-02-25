import { RelationItem } from '~/domain/models/tasks/relation'

export interface RelationRepository {
    list(projectId: string, exampleId: number): Promise<RelationItem[]>

    create(projectId: string, exampleId: number, relation: RelationItem): Promise<RelationItem>

    update(projectId: string, exampleId: number, relationId: number, relationType: number): Promise<RelationItem>

    delete(projectId: string, exampleId: number, relationId: number): Promise<void>

    bulkDelete(projectId: string, exampleId: number, relationIds: number[]): Promise<void>
}
