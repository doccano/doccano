import { Plugin } from '@nuxt/types'
import { FromApiLabelItemListRepository } from '@/repositories/label/api'
import { FromApiMemberItemListRepository } from '@/repositories/member/api'
import { LabelApplicationService } from '@/services/application/label.service'
import { MemberApplicationService } from '@/services/application/member.service'

export interface Services {
  label: LabelApplicationService,
  member: MemberApplicationService
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $services: Services
  }
}

const plugin: Plugin = (context, inject) => {
  const labelRepository = new FromApiLabelItemListRepository()
  const label = new LabelApplicationService(labelRepository)
  const memberRepository = new FromApiMemberItemListRepository()
  const member = new MemberApplicationService(memberRepository)
  const services: Services = {
    label,
    member
  }
  inject('services', services)
}

export default plugin
