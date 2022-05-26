import { computed, reactive } from '@nuxtjs/composition-api'
import { LabelDTO } from '@/services/application/label/labelData'
import { CreateLabelCommand, UpdateLabelCommand } from '@/services/application/label/labelCommand'
import { LabelApplicationService } from '@/services/application/label/labelApplicationService'

export const useLabelList = (service: LabelApplicationService) => {
  const state = reactive({
    labels: [] as LabelDTO[]
  })

  const getLabelList = async (projectId: string) => {
    state.labels = await service.list(projectId)
  }

  const createLabel = async (projectId: string, command: CreateLabelCommand) => {
    await service.create(projectId, command)
    await getLabelList(projectId)
  }

  const updateLabel = async (projectId: string, command: UpdateLabelCommand) => {
    await service.update(projectId, command)
  }

  const deleteLabelList = async (projectId: string, items: LabelDTO[]) => {
    await service.bulkDelete(projectId, items)
    await getLabelList(projectId)
  }

  const findLabelById = (labelId: number) => {
    return state.labels.find((item) => item.id === labelId)
  }

  const shortKeys = computed(() => {
    return Object.fromEntries(state.labels.map((item) => [item.id, [item.suffixKey]]))
  })

  return {
    state,
    getLabelList,
    findLabelById,
    createLabel,
    updateLabel,
    deleteLabelList,
    shortKeys
  }
}
