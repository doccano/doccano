import { computed, ref } from '@nuxtjs/composition-api'
import { LabelRepository } from '@/domain/models/label/labelRepository'
import { LabelItem } from '@/domain/models/label/label'

export const useLabelType = (repository: LabelRepository) => {
  const labelTypes = ref<LabelItem[]>([])
  const isLoading = ref(false)

  const fetchLabelTypes = async (projectId: string) => {
    isLoading.value = true
    labelTypes.value = await repository.list(projectId)
    isLoading.value = false
  }

  const createLabelType = async (projectId: string, labelType: LabelItem) => {
    await repository.create(projectId, labelType)
    await fetchLabelTypes(projectId)
  }

  const updateLabelType = async (projectId: string, labelType: LabelItem) => {
    await repository.update(projectId, labelType)
    await fetchLabelTypes(projectId)
  }

  const deleteLabelTypes = async (projectId: string, items: LabelItem[]) => {
    await repository.bulkDelete(
      projectId,
      items.map((item) => item.id)
    )
    await fetchLabelTypes(projectId)
  }

  const findLabelTypeById = async (projectId: string, labelTypeId: number) => {
    return await repository.findById(projectId, labelTypeId)
  }

  const usedShortKeys = computed(() => {
    return Object.fromEntries(labelTypes.value.map((item) => [item.id, [item.suffixKey]]))
  })

  return {
    labelTypes,
    isLoading,
    createLabelType,
    fetchLabelTypes,
    updateLabelType,
    deleteLabelTypes,
    findLabelTypeById,
    usedShortKeys
  }
}
