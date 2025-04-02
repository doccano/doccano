export interface Disagreement {
    id: number;
    dataset_item_id: number;
    annotations: number[];
    disagreement_details?: any;
    status: string;
    resolved_by?: number | null;
    resolution_comments?: string;
    created_at: string;
    updated_at: string;
    resolved_at?: string | null;
  }