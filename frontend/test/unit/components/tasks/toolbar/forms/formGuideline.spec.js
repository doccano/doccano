/**
 * @jest-environment jsdom
 */
import { mount } from '@vue/test-utils'
import FormGuideline from '@/components/tasks/toolbar/forms/FormGuideline'

const $t = () => {}

const factory = () => {
  return mount(FormGuideline, {
    propsData: {
      guidelineText: 'Hello'
    },
    mocks: { $t }
  })
}

describe('FormGuideline test', () => {
  it('display guideline text', () => {
    const wrapper = factory()
    expect(wrapper.find('.tui-editor-contents').text()).toEqual('Hello')
  })
})
