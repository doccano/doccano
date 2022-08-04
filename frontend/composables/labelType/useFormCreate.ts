import { ref, useRouter } from '@nuxtjs/composition-api'
import { LabelRepository } from '@/domain/models/label/labelRepository'
import { LabelItem } from '@/domain/models/label/label'
import { useLabelType } from './useLabelType'

export const useFormCreate = (repository: LabelRepository) => {
  const { labelTypes, createLabelType, fetchLabelTypes } = useLabelType(repository)
  const editedItem = ref<LabelItem>(LabelItem.create())
  const router = useRouter()

  const save = async (projectId: string) => {
    await createLabelType(projectId, editedItem.value)
    router.push(`/projects/${projectId}/labels`)
  }

  const saveAndAnother = async (projectId: string) => {
    await createLabelType(projectId, editedItem.value)
    editedItem.value = LabelItem.create()
    await fetchLabelTypes(projectId)
  }

  return {
    fetchLabelTypes,
    save,
    saveAndAnother,
    labelTypes,
    editedItem
  }
}
