export interface ParseRepository {
  analyze(
    projectId: string,
    format: string,
    task: string,
    uploadIds: number[],
    option: object
  ): Promise<string>

  revert(serverId: string): void
}
