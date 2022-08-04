import { ref, useRouter } from '@nuxtjs/composition-api'
import { LabelRepository } from '@/domain/models/label/labelRepository'
import { LabelItem } from '@/domain/models/label/label'
import { useLabelType } from './useLabelType'

export const useFormEdit = (repository: LabelRepository) => {
  const { labelTypes, updateLabelType, fetchLabelTypes, findLabelTypeById } =
    useLabelType(repository)
  const editedItem = ref<LabelItem>(LabelItem.create())
  const router = useRouter()

  const save = async (projectId: string): Promise<void> => {
    await updateLabelType(projectId, editedItem.value)
    router.push(`/projects/${projectId}/labels`)
  }

  return {
    fetchLabelTypes,
    findLabelTypeById,
    save,
    labelTypes,
    editedItem
  }
}
