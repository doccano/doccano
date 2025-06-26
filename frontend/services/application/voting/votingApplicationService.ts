import { VotingConfiguration, VotingConfigurationData } from '@/domain/models/voting/votingConfiguration'
import { Vote, VoteData, UserVoteStatus } from '@/domain/models/voting/vote'
import { VotingResults } from '@/domain/models/voting/votingResults'
import { APIVotingRepository } from '@/repositories/voting/apiVotingRepository'

export class VotingApplicationService {
  constructor(private readonly repository: APIVotingRepository) {}

  public async list(projectId: string): Promise<VotingConfiguration[]> {
    try {
      return await this.repository.list(projectId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async findById(projectId: string, configId: string): Promise<VotingConfiguration> {
    try {
      return await this.repository.findById(projectId, configId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async create(projectId: string, data: VotingConfigurationData): Promise<VotingConfiguration> {
    try {
      return await this.repository.create(projectId, data)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(projectId: string, configId: string, data: VotingConfigurationData): Promise<VotingConfiguration> {
    try {
      return await this.repository.update(projectId, configId, data)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async delete(projectId: string, configId: string): Promise<void> {
    try {
      await this.repository.delete(projectId, configId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async getResults(projectId: string, configId: string): Promise<VotingResults[]> {
    try {
      return await this.repository.getResults(projectId, configId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async getUserVotes(projectId: string, configId: string): Promise<UserVoteStatus[]> {
    try {
      return await this.repository.getUserVotes(projectId, configId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async submitVote(projectId: string, configId: string, data: VoteData): Promise<Vote> {
    try {
      return await this.repository.submitVote(projectId, configId, data)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async removeVote(projectId: string, configId: string, ruleId: string): Promise<void> {
    try {
      await this.repository.removeVote(projectId, configId, ruleId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async getActiveConfigurations(projectId: string): Promise<VotingConfiguration[]> {
    try {
      return await this.repository.getActiveConfigurations(projectId)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }
}
