import _ from 'lodash'
import { reactive, useContext } from '@nuxtjs/composition-api'
import { ExampleDTO } from '@/services/application/example/exampleData'

export const useExampleItem = () => {
  const state = reactive({
    example: {} as ExampleDTO,
    totalExample: 0
  })

  const { app } = useContext()
  const exampleService = app.$services.example

  const getExample = async(
    projectId: string,
    filterOption: string,
    { page, q, isChecked }: { page: string, q: string, isChecked: string}
  ) => {
    const examples = await exampleService.fetchOne(projectId, page, q, isChecked, filterOption)
    state.totalExample = examples.count
    if (!_.isEmpty(examples) && examples.items.length !== 0) {
      state.example = examples.items[0]
    }
  }

  const getExampleById = async(
    projectId: string
  ) => {
    state.example = await exampleService.findById(projectId, state.example.id)
  }

  const approve = async(
    projectId: string,
  ) => {
    const approved = !state.example.isApproved
    await exampleService.approve(projectId, state.example.id, approved)
    await getExampleById(projectId)
  }

  return {
    state,
    approve,
    getExample,
  }
}
