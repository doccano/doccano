import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import ProjectCreationButton from '@/components/containers/ProjectCreationButton'
const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)

describe('ProjectCreationButtonContainer', () => {
  let store
  let projects
  let actions
  let mutations

  beforeEach(() => {
    actions = {
      createProject: jest.fn()
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

  test('called createProject action', () => {
    const wrapper = shallowMount(ProjectCreationButton, { store, localVue })
    wrapper.vm.createProject()
    expect(actions.createProject).toHaveBeenCalled()
  })
})
