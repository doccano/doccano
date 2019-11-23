import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import ProjectDeletionButton from '@/components/containers/ProjectDeletionButton'
const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)

describe('ProjectDeletionButtonContainer', () => {
  let store
  let projects
  let actions
  let mutations

  beforeEach(() => {
    actions = {
      deleteProject: jest.fn()
    }
    mutations = {}
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

  test('called deleteProject action', () => {
    const wrapper = shallowMount(ProjectDeletionButton, { store, localVue })
    wrapper.vm.handleDeleteProject()
    expect(actions.deleteProject).toHaveBeenCalled()
  })
})
