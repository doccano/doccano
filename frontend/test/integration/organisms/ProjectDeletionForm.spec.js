import { mount } from '@vue/test-utils'
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
    return mount(ProjectDeletionForm, {
      propsData: {
        ...propsData
      }
    })
  }

  test('emit close event when cancel button is clicked', () => {
    const wrapper = factory({ selected })
    const button = wrapper.find('[data-test="cancel-button"]')
    button.trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  test('emit delete event when delete button is clicked', () => {
    const wrapper = factory({ selected })
    const button = wrapper.find('[data-test="delete-button"]')
    button.trigger('click')
    expect(wrapper.emitted('delete')).toBeTruthy()
  })
})
