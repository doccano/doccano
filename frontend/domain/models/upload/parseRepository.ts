export interface ParseRepository {
  analyze(projectId: string, format: string, uploadIds: number[], option: object): Promise<string>

  revert(serverId: string): void
}
