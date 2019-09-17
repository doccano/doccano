import { shallowMount } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import ProjectList from '@/components/organisms/ProjectList'

Vue.use(Vuetify)

describe('ProjectList', () => {
  const projects = [
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
    }
  ]
  const headers = [
    {
      text: 'Name',
      align: 'left',
      value: 'name'
    },
    {
      text: 'Description',
      value: 'description'
    },
    {
      text: 'Type',
      value: 'project_type'
    }
  ]
  const selected = []
  const loading = false

  test('can receive props', () => {
    const propsData = { projects, headers, selected, loading }
    const wrapper = shallowMount(ProjectList, { propsData })
    expect(wrapper.props()).toEqual(propsData)
  })

  test('emitted update event', () => {
    const propsData = { projects, headers, selected, loading }
    const wrapper = shallowMount(ProjectList, { propsData })
    wrapper.vm.update(propsData)
    expect(wrapper.emitted('update')).toBeTruthy()
  })

  test('raise warning when passing props', () => {
    const spy = jest.spyOn(console, 'error')
    spy.mockImplementation()
    const wrapper = shallowMount(ProjectList)
    expect(spy).toBeCalledWith(
      expect.stringContaining('[Vue warn]: Missing required prop')
    )
    spy.mockRestore()
  })
})
