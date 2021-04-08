export interface ParseRepository {
  analyze(projectId: string, format: string, uploadIds: number[]): Promise<string>
}
