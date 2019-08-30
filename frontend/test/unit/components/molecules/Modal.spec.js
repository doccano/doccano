import { shallowMount } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import Modal from '@/components/Modal.vue'

Vue.use(Vuetify)

describe('Modal', () => {
  test('can receive props', () => {
    const propsData = {
      title: 'test title',
      button: 'test text'
    }
    const wrapper = shallowMount(Modal, { propsData })
    expect(wrapper.props()).toEqual(propsData)
  })

  test('can insert content into slot', () => {
    const wrapper = shallowMount(Modal, {
      slots: {
        default: '<div data-test="slotContent">slot content</div>'
      }
    })
    const slotContent = wrapper.find('[data-test="slotContent"]')
    expect(slotContent.exists()).toBe(true)
    expect(slotContent.text()).toBe('slot content')
  })

  test('is closed by default', () => {
    const wrapper = shallowMount(Modal)
    expect(wrapper.vm.dialog).toBe(false)
  })

  test('can open dialog', () => {
    const wrapper = shallowMount(Modal)
    wrapper.vm.open()
    expect(wrapper.vm.dialog).toBe(true)
  })

  test('can close after agree', () => {
    const wrapper = shallowMount(Modal)
    wrapper.vm.open()
    expect(wrapper.vm.dialog).toBe(true)
    wrapper.vm.agree()
    expect(wrapper.vm.dialog).toBe(false)
  })

  test('can close after cancel', () => {
    const wrapper = shallowMount(Modal)
    wrapper.vm.open()
    expect(wrapper.vm.dialog).toBe(true)
    wrapper.vm.cancel()
    expect(wrapper.vm.dialog).toBe(false)
  })
})
