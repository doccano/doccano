import { VotingConfiguration, VotingConfigurationData } from '~/domain/models/voting/votingConfiguration'
import { Vote, VoteData, UserVoteStatus } from '~/domain/models/voting/vote'
import { VotingResults } from '~/domain/models/voting/votingResults'
import ApiService from '@/services/api.service'

function toVotingConfigurationModel(item: { [key: string]: any }): VotingConfiguration {
  return {
    id: item.id,
    name: item.name,
    description: item.description,
    voting_method: item.voting_method,
    start_date: item.start_date,
    end_date: item.end_date,
    start_time: item.start_time,
    end_time: item.end_time,
    status: item.status,
    created_at: item.created_at,
    updated_at: item.updated_at,
    annotation_rules: item.annotation_rules || []
  }
}

function toVoteModel(item: { [key: string]: any }): Vote {
  return {
    id: item.id,
    annotation_rule: item.annotation_rule,
    user: item.user,
    username: item.username,
    vote: item.vote,
    created_at: item.created_at,
    updated_at: item.updated_at
  }
}

function toVotingResultsModel(item: { [key: string]: any }): VotingResults {
  return {
    rule_id: item.rule_id,
    rule_name: item.rule_name,
    total_votes: item.total_votes,
    approve_votes: item.approve_votes,
    disapprove_votes: item.disapprove_votes,
    neutral_votes: item.neutral_votes,
    approval_percentage: item.approval_percentage
  }
}

function toUserVoteStatusModel(item: { [key: string]: any }): UserVoteStatus {
  return {
    configuration_id: item.configuration_id,
    rule_id: item.rule_id,
    vote: item.vote,
    voted_at: item.voted_at
  }
}

export class APIVotingRepository {
  constructor(private readonly apiService = ApiService) {}

  async list(projectId: string): Promise<VotingConfiguration[]> {
    const url = `/projects/${projectId}/voting/`
    const response = await this.apiService.get(url)
    return response.data.results.map(toVotingConfigurationModel)
  }

  async findById(projectId: string, configId: string): Promise<VotingConfiguration> {
    const url = `/projects/${projectId}/voting/${configId}/`
    const response = await this.apiService.get(url)
    return toVotingConfigurationModel(response.data)
  }

  async create(projectId: string, data: VotingConfigurationData): Promise<VotingConfiguration> {
    const url = `/projects/${projectId}/voting/`
    const response = await this.apiService.post(url, data)
    return toVotingConfigurationModel(response.data)
  }

  async update(projectId: string, configId: string, data: VotingConfigurationData): Promise<VotingConfiguration> {
    const url = `/projects/${projectId}/voting/${configId}/`
    const response = await this.apiService.put(url, data)
    return toVotingConfigurationModel(response.data)
  }

  async delete(projectId: string, configId: string): Promise<void> {
    const url = `/projects/${projectId}/voting/${configId}/`
    await this.apiService.delete(url)
  }

  async getResults(projectId: string, configId: string): Promise<VotingResults[]> {
    const url = `/projects/${projectId}/voting/${configId}/results/`
    const response = await this.apiService.get(url)
    return response.data.map(toVotingResultsModel)
  }

  async getUserVotes(projectId: string, configId: string): Promise<UserVoteStatus[]> {
    const url = `/projects/${projectId}/voting/${configId}/user-votes/`
    const response = await this.apiService.get(url)
    return response.data.map(toUserVoteStatusModel)
  }

  async submitVote(projectId: string, configId: string, data: VoteData): Promise<Vote> {
    const url = `/projects/${projectId}/voting/${configId}/vote/`
    const response = await this.apiService.post(url, data)
    return toVoteModel(response.data.vote)
  }

  async removeVote(projectId: string, configId: string, ruleId: string): Promise<void> {
    const url = `/projects/${projectId}/voting/${configId}/vote/${ruleId}/`
    await this.apiService.delete(url)
  }

  async getActiveConfigurations(projectId: string): Promise<VotingConfiguration[]> {
    const url = `/projects/${projectId}/voting/active/`
    const response = await this.apiService.get(url)
    return response.data.map(toVotingConfigurationModel)
  }
}
