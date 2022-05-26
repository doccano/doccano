export type Label = { [key: string]: number }
export type User = { [key: string]: number }
export type ConfirmedCount = { [key: string]: number }
export type Distribution = { [user: string]: { [label: string]: number } }
export interface Progress {
  total: number
  progress: { user: string; done: number }[]
}

export interface MyProgress {
  total: number
  complete: number
  remaining: number
}
