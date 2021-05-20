import { computed, reactive, ref, useContext } from '@nuxtjs/composition-api'
import { LabelDTO } from '@/services/application/label/labelData'
import { CreateLabelCommand , UpdateLabelCommand } from '@/services/application/label/labelCommand'


export const useLabelList = () => {
  const state = reactive({
    labels: [] as LabelDTO[]
  })

  const { app } = useContext()
  const $services = app.$services

  const getLabelList = async(
    projectId: string
  ) => {
    state.labels = await $services.label.list(projectId)
  }

  const createLabel = async(
    projectId: string,
    command: CreateLabelCommand
  ) => {
    await $services.label.create(projectId, command)
    await getLabelList(projectId)
  }

  const updateLabel = async(
    projectId: string,
    command: UpdateLabelCommand
  ) => {
    await $services.label.update(projectId, command)
  }

  const deleteLabelList = async(
    projectId: string,
    items: LabelDTO[]
  ) => {
    await $services.label.bulkDelete(projectId, items)
    await getLabelList(projectId)
  }

  const findLabelById = (labelId: number) => {
    return state.labels.find(item => item.id === labelId)
  }

  const shortKeys = computed(() => {
    return Object.fromEntries(state.labels.map(item => [item.id, [item.suffixKey]]))
  })

  return {
    state,
    getLabelList,
    findLabelById,
    createLabel,
    updateLabel,
    deleteLabelList,
    shortKeys,
  }
}
