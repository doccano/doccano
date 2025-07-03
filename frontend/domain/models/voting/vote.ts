export interface Vote {
  id: number
  annotation_rule: number
  user: number
  username: string
  vote: 'approve' | 'disapprove' | 'neutral'
  created_at: string
  updated_at: string
}

export interface VoteData {
  rule_id: number
  vote: 'approve' | 'disapprove' | 'neutral' | null
}

export interface UserVoteStatus {
  configuration_id: number
  rule_id: number
  vote: 'approve' | 'disapprove' | 'neutral'
  voted_at: string
}
