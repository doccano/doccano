import { reactive, useContext } from '@nuxtjs/composition-api'
import { Project } from '~/domain/models/project/project'

export const useProjectItem = () => {
  const state = reactive({
    project: {} as Project
  })

  const { app } = useContext()
  const projectService = app.$services.project

  const getProjectById = async (projectId: string) => {
    state.project = await projectService.findById(projectId)
  }

  return {
    state,
    getProjectById
  }
}
