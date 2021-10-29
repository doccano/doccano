/**
 * @jest-environment jsdom
 */
import { mount } from '@vue/test-utils'
import FormGuideline from '@/components/tasks/toolbar/forms/FormGuideline'

const $t = () => {}

const factory = (values = {}) => {
  return mount(FormGuideline, {
    propsData: {
      guidelineText: 'Hello'
    },
    mocks:{ $t }
  })
}

describe('Foo', () => {
  it('welcome メッセージを描画する', () => {
    const wrapper = factory()
    expect(wrapper.find('.tui-editor-contents').text()).toEqual('Hello')
  })
})
