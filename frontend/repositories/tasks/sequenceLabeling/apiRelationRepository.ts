import ApiService from '@/services/api.service'
import { RelationRepository } from "~/domain/models/tasks/relationRepository"
import { RelationItem } from "~/domain/models/tasks/relation"

export class ApiRelationRepository implements RelationRepository {
    constructor(
        private readonly request = ApiService
    ) {
    }

    async list(projectId: string, exampleId: number): Promise<RelationItem[]> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations`
        const response = await this.request.get(url)
        return response.data.map((relation: any) => RelationItem.valueOf(relation))
    }

    async create(projectId: string, exampleId: number, item: RelationItem): Promise<RelationItem> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations`
        const response = await this.request.post(url, item.toObject())
        return RelationItem.valueOf(response.data)
    }

    async update(projectId: string, exampleId: number, relationId: number, relationType: number): Promise<RelationItem> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations/${relationId}`
        const response = await this.request.patch(url, {type: relationType})
        return RelationItem.valueOf(response.data)
    }

    async delete(projectId: string, exampleId: number, relationId: number): Promise<void> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations/${relationId}`
        const response = await this.request.delete(url)
    }

    async bulkDelete(projectId: string, exampleId: number, relationIds: number[]): Promise<void> {
        const url = `/projects/${projectId}/examples/${exampleId}/relations`
        await this.request.delete(url, {ids: relationIds})
    }
}
