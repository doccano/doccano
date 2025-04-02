export interface Annotation {
  id: number;
  dataset_item_id: number;
  annotator: number; // or string, depending on your user identity
  extracted_labels?: any;
  additional_info?: any;
  created_at: string;
  updated_at: string;
}