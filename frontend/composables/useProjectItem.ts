import { reactive, useContext } from '@nuxtjs/composition-api'
import { ProjectDTO } from '@/services/application/project/projectData'

export const useProjectItem = () => {
  const state = reactive({
    project: {} as ProjectDTO
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
