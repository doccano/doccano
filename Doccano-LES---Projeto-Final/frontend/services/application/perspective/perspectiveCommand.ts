import { PerspectiveDTO } from './perspectiveData'

export type CreatePerspectiveCommand = Omit<PerspectiveDTO, 'id'>

export type ListPerspectiveCommand = {
  projectId: string
  username?: string
}
