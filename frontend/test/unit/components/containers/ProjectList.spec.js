import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import ProjectList from '@/components/containers/ProjectList'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('ProjectListContainer', () => {
  let store
  let projects
  let actions
  let mutations

  beforeEach(() => {
    actions = {
      getProjectList: jest.fn()
    }
    mutations = {
      updateSelected: jest.fn()
    }
    projects = {
      namespaced: true,
      actions,
      mutations,
      state: {}
    }

    store = new Vuex.Store({
      modules: {
        projects
      }
    })
  })

  test('called updateSelected method', () => {
    const wrapper = shallowMount(ProjectList, { store, localVue })
    wrapper.vm.update()
    expect(mutations.updateSelected).toHaveBeenCalled()
  })
})
