import ApiService from '@/services/api.service'
import { Group, GroupDetails, Permission, ContentType } from '@/domain/models/group/group'
import { PaginatedResponse } from '@/repositories/user/apiUserRepository'

function toGroupModel(item: { [key: string]: any }): Group {
    return new Group(
        item.id,
        item.name
    )
}

function toGroupDetailsModel(item: { [key: string]: any }): GroupDetails {
    return new GroupDetails(
        item.id,
        item.name,
        item.permissions,
        item.permission_names
    )
}

function toPermissionModel(item: { [key: string]: any }): Permission {
    return new Permission(
        item.id,
        item.name,
        item.codename,
        item.content_type,
        item.label
    )
}

function toContentTypeModel(item: { [key: string]: any }): ContentType {
    return new ContentType(
        item.id,
        item.app_label,
        item.model
    )
}

function toGroupModelList(response: PaginatedResponse<any>): PaginatedResponse<Group> {
    return {
        count: response.count,
        next: response.next,
        previous: response.previous,
        results: response.results.map((item: any) => toGroupModel(item))
    }
}

function toPermissionModelList(response: PaginatedResponse<any>): PaginatedResponse<Permission> {
    return {
        count: response.count,
        next: response.next,
        previous: response.previous,
        results: response.results.map((item: any) => toPermissionModel(item))
    }
}

function toContentTypeModelList(response: PaginatedResponse<any>): PaginatedResponse<ContentType> {
    return {
        count: response.count,
        next: response.next,
        previous: response.previous,
        results: response.results.map((item: any) => toContentTypeModel(item))
    }
}

export class APIGroupRepository {
    constructor(private readonly request = ApiService) { }

    // Group methods
    async listGroups(query: string = ''): Promise<PaginatedResponse<Group>> {
        const url = `/groups/?${query}`
        const response = await this.request.get(url)
        return toGroupModelList(response.data)
    }

    async getGroup(id: number): Promise<GroupDetails> {
        const url = `/groups/${id}/`
        const response = await this.request.get(url)
        return toGroupDetailsModel(response.data)
    }

    async createGroup(data: { name: string, permissions?: number[] }): Promise<Group> {
        const url = '/groups/'
        // Ensure permissions is sent as an array even if empty
        const payload = {
            name: data.name,
            permissions: data.permissions || []
        }
        const response = await this.request.post(url, payload)
        return toGroupModel(response.data)
    }

    async updateGroup(id: number, data: { name?: string, permissions?: number[] }): Promise<Group> {
        const url = `/groups/${id}/`
        // Ensure permissions is sent as an array even if empty
        const payload = { ...data }
        if (!payload.permissions) {
            payload.permissions = []
        }
        const response = await this.request.patch(url, payload)
        return toGroupModel(response.data)
    }

    async deleteGroup(id: number): Promise<void> {
        const url = `/groups/${id}/`
        await this.request.delete(url)
    }

    // Permission methods
    async listPermissions(query: string = ''): Promise<PaginatedResponse<Permission>> {
        const url = `/permissions/?${query}`
        const response = await this.request.get(url)
        return toPermissionModelList(response.data)
    }

    async getPermission(id: number): Promise<Permission> {
        const url = `/permissions/${id}/`
        const response = await this.request.get(url)
        return toPermissionModel(response.data)
    }

    // ContentType methods
    async listContentTypes(query: string = ''): Promise<PaginatedResponse<ContentType>> {
        const url = `/content-types/?${query}`
        const response = await this.request.get(url)
        return toContentTypeModelList(response.data)
    }

    async getContentType(id: number): Promise<ContentType> {
        const url = `/content-types/${id}/`
        const response = await this.request.get(url)
        return toContentTypeModel(response.data)
    }
}