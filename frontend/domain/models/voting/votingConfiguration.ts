export interface AnnotationRule {
  id: number
  name: string
  description: string
  order: number
}

export interface AnnotationRuleData {
  name: string
  description: string
  order?: number
}

export interface VotingConfiguration {
  id: number
  name: string
  description: string
  voting_method: 'approve_only' | 'disapprove_only' | 'approve_disapprove'
  start_date: string
  end_date: string
  start_time: string
  end_time: string
  status: 'configured' | 'active' | 'ended'
  created_at: string
  updated_at: string
  annotation_rules: AnnotationRule[]
}

export interface VotingConfigurationData {
  name: string
  description: string
  voting_method: 'approve_only' | 'disapprove_only' | 'approve_disapprove'
  start_date: string
  end_date: string
  start_time: string
  end_time: string
  status?: 'configured' | 'active' | 'ended'
  annotation_rules: AnnotationRuleData[]
}
