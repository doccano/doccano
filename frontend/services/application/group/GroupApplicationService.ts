import { Group, GroupDetails, Permission, ContentType } from '@/domain/models/group/group'
import { APIGroupRepository } from '@/repositories/group/apiGroupRepository'
import { PaginatedResponse } from '@/repositories/user/apiUserRepository'

export class GroupApplicationService {
    constructor(private readonly repository: APIGroupRepository) { }

    // Group methods
    public async listGroups(query: string = ''): Promise<PaginatedResponse<Group>> {
        try {
            return await this.repository.listGroups(query)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || 'Failed to fetch groups')
        }
    }

    public async getGroup(id: number): Promise<GroupDetails> {
        try {
            return await this.repository.getGroup(id)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || `Failed to fetch group with ID ${id}`)
        }
    }

    public async createGroup(data: { name: string, permissions?: number[] }): Promise<Group> {
        try {
            return await this.repository.createGroup(data)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || 'Failed to create group')
        }
    }

    public async updateGroup(id: number, data: { name?: string, permissions?: number[] }): Promise<Group> {
        try {
            return await this.repository.updateGroup(id, data)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || `Failed to update group with ID ${id}`)
        }
    }

    public async deleteGroup(id: number): Promise<void> {
        try {
            await this.repository.deleteGroup(id)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || `Failed to delete group with ID ${id}`)
        }
    }

    // Permission methods
    public async listPermissions(query: string = ''): Promise<PaginatedResponse<Permission>> {
        try {
            return await this.repository.listPermissions(query)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || 'Failed to fetch permissions')
        }
    }

    public async getPermission(id: number): Promise<Permission> {
        try {
            return await this.repository.getPermission(id)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || `Failed to fetch permission with ID ${id}`)
        }
    }

    // ContentType methods
    public async listContentTypes(query: string = ''): Promise<PaginatedResponse<ContentType>> {
        try {
            return await this.repository.listContentTypes(query)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || 'Failed to fetch content types')
        }
    }

    public async getContentType(id: number): Promise<ContentType> {
        try {
            return await this.repository.getContentType(id)
        } catch (e: any) {
            throw new Error(e.response?.data?.detail || `Failed to fetch content type with ID ${id}`)
        }
    }
}