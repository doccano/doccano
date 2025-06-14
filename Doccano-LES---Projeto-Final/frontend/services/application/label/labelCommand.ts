import { LabelDTO } from './labelData'

export type CreateLabelCommand = Omit<LabelDTO, 'id'>
export type UpdateLabelCommand = LabelDTO
