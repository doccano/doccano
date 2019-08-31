import { shallowMount } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import ProjectDeletionForm from '@/components/organisms/ProjectDeletionForm'

Vue.use(Vuetify)

describe('ProjectDeletionForm', () => {
  const selected = [
    {
      id: 1,
      name: 'CoNLL 2003',
      description: 'This is a project for NER.',
      guideline: 'Please write annotation guideline.',
      users: [
        1
      ],
      project_type: 'SequenceLabeling',
      image: '/static/assets/images/cats/sequence_labeling.jpg',
      updated_at: '2019-07-09T06:19:29.789091Z',
      randomize_document_order: false,
      resourcetype: 'SequenceLabelingProject'
    },
  ]
  const factory = (propsData) => {
    return shallowMount(ProjectDeletionForm, {
      propsData: {
        ...propsData
      }
    })
  }

  test('can receive props', () => {
    const wrapper = factory({ selected })
    expect(wrapper.props()).toEqual({ selected })
  })

  test('emit close event', () => {
    const wrapper = factory({ selected })
    wrapper.vm.cancel(selected)
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  test('emit delete event', () => {
    const wrapper = factory({ selected })
    wrapper.vm.deleteProject(selected)
    expect(wrapper.emitted('delete')).toBeTruthy()
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
