import { Plugin } from '@nuxt/types'
import { FromApiLabelItemListRepository } from '@/repositories/label/api'
import { LabelApplicationService } from '@/services/application/label.service'

export interface Services {
  label: LabelApplicationService
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $services: Services
  }
}

const plugin: Plugin = (context, inject) => {
  const labelRepository = new FromApiLabelItemListRepository()
  const label = new LabelApplicationService(labelRepository)
  const services: Services = {
    label
  }
  inject('services', services)
}

export default plugin
