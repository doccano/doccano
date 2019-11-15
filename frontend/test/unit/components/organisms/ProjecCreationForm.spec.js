import { shallowMount } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import ProjectCreationForm from '@/components/organisms/ProjectCreationForm'

Vue.use(Vuetify)

describe('ProjectCreationForm', () => {
  const factory = (propsData) => {
    return shallowMount(ProjectCreationForm, {
      propsData: {
        ...propsData
      }
    })
  }
  const createProject = () => { }
  const projectTypes = []

  test('can receive props', () => {
    const wrapper = factory({ createProject, projectTypes })
    expect(wrapper.props()).toEqual({ createProject, projectTypes })
  })

  test('emit close event', () => {
    const wrapper = factory({ createProject, projectTypes })
    wrapper.vm.cancel()
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  test('emit close event when form is valid', () => {
    const wrapper = factory({ createProject, projectTypes })
    wrapper.setMethods({
      validate: jest.fn(() => true),
      reset: jest.fn()
    })
    wrapper.vm.create()
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  test('do not emit close event when form is invalid', () => {
    const wrapper = factory({ createProject, projectTypes })
    wrapper.setMethods({
      validate: jest.fn(() => false),
      reset: jest.fn()
    })
    wrapper.vm.create()
    expect(wrapper.emitted('close')).toBeFalsy()
  })

  test('raise warning when passing no props', () => {
    const spy = jest.spyOn(console, 'error')
    spy.mockImplementation()
    const wrapper = factory()
    expect(spy).toBeCalledWith(
      expect.stringContaining('[Vue warn]: Missing required prop')
    )
    spy.mockRestore()
  })
})
