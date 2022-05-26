import { reactive } from '@nuxtjs/composition-api'

export const useTeacherList = (service: any) => {
  const state = reactive({
    teacherList: []
  })

  const getTeacherList = async (projectId: string, exampleId: number) => {
    state.teacherList = await service.list(projectId, exampleId)
  }

  const removeTeacher = async (projectId: string, exampleId: number, teacherId: number) => {
    await service.delete(projectId, exampleId, teacherId)
    await getTeacherList(projectId, exampleId)
  }

  const annotateLabel = async (projectId: string, exampleId: number, labelId: number) => {
    await service.create(projectId, exampleId, labelId)
    await getTeacherList(projectId, exampleId)
  }

  const clearTeacherList = async (projectId: string, exampleId: number) => {
    await service.clear(projectId, exampleId)
    await getTeacherList(projectId, exampleId)
  }

  const autoLabel = async (projectId: string, exampleId: number) => {
    await service.autoLabel(projectId, exampleId)
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
