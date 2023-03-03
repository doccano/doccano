import { reactive } from '@nuxtjs/composition-api'
import { Category } from '~/domain/models/tasks/category'

export const useTeacherList = (repository: any) => {
  const state = reactive({
    teacherList: []
  })

  const getTeacherList = async (projectId: string, exampleId: number) => {
    state.teacherList = await repository.list(projectId, exampleId)
  }

  const removeTeacher = async (projectId: string, exampleId: number, teacherId: number) => {
    await repository.delete(projectId, exampleId, teacherId)
    await getTeacherList(projectId, exampleId)
  }

  const annotateLabel = async (projectId: string, exampleId: number, labelId: number) => {
    const category = Category.create(labelId)
    await repository.create(projectId, exampleId, category)
    await getTeacherList(projectId, exampleId)
  }

  const clearTeacherList = async (projectId: string, exampleId: number) => {
    await repository.clear(projectId, exampleId)
    await getTeacherList(projectId, exampleId)
  }

  const autoLabel = async (projectId: string, exampleId: number) => {
    await repository.autoLabel(projectId, exampleId)
    await getTeacherList(projectId, exampleId)
  }

  const annotateOrRemoveLabel = async (projectId: string, exampleId: number, srcKey: string) => {
    const labelId = parseInt(srcKey, 10)
    // @ts-ignore
    const annotation = state.teacherList.find((item) => item.label === labelId)
    if (annotation) {
      // @ts-ignore
      await removeTeacher(projectId, exampleId, annotation.id)
    } else {
      await annotateLabel(projectId, exampleId, labelId)
    }
  }

  return {
    state,
    getTeacherList,
    annotateLabel,
    annotateOrRemoveLabel,
    removeTeacher,
    clearTeacherList,
    autoLabel
  }
}
