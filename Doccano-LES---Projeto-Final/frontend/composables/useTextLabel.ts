import { reactive } from '@nuxtjs/composition-api'
import { TextLabel } from '~/domain/models/tasks/textLabel'

export const useTextLabel = (repository: any, projectId: string) => {
  const state = reactive({
    labels: [] as TextLabel[],
    error: ''
  })

  const validateText = (text: string) => {
    if (state.labels.some((label) => label.text === text)) {
      state.error = 'The label already exists.'
      return false
    }
    return true
  }

  const add = async (exampleId: number, text: string) => {
    const textLabel = TextLabel.create(text)
    if (!validateText(textLabel.text)) {
      return
    }
    try {
      await repository.create(projectId, exampleId, textLabel)
      await list(exampleId)
    } catch (e: any) {
      state.error = e.response.data.detail
    }
  }

  const list = async (exampleId: number) => {
    state.labels = await repository.list(projectId, exampleId)
  }

  const update = async (exampleId: number, labelId: number, text: string) => {
    if (!validateText(text)) {
      return
    }
    const label = state.labels.find((label) => label.id === labelId)!
    label.updateText(text)
    try {
      await repository.update(projectId, exampleId, labelId, label)
      await list(exampleId)
    } catch (e: any) {
      state.error = e.response.data.detail
    }
  }

  const remove = async (exampleId: number, labelId: number) => {
    await repository.delete(projectId, exampleId, labelId)
    state.labels = state.labels.filter((label) => label.id !== labelId)
  }

  const clear = async (exampleId: number) => {
    await repository.clear(projectId, exampleId)
    state.labels = []
  }

  const autoLabel = async (exampleId: number) => {
    try {
      await repository.autoLabel(projectId, exampleId)
      await list(exampleId)
    } catch (e: any) {
      state.error = e.response.data.detail
    }
  }

  return {
    state,
    add,
    list,
    update,
    remove,
    clear,
    autoLabel
  }
}
