import { Plugin } from '@nuxt/types'
import { FromApiLabelItemListRepository } from '@/repositories/label/api'
import { FromApiMemberItemListRepository } from '@/repositories/member/api'
import { FromApiUserItemListRepository } from '@/repositories/user/api'
import { FromApiRoleItemListRepository } from '@/repositories/role/api'
import { FromApiProjectItemListRepository } from '@/repositories/project/api'
import { FromApiCommentItemListRepository } from '@/repositories/comment/api'
import { LabelApplicationService } from '@/services/application/label.service'
import { MemberApplicationService } from '@/services/application/member.service'
import { UserApplicationService } from '@/services/application/user.service'
import { RoleApplicationService } from '@/services/application/role.service'
import { ProjectApplicationService } from '@/services/application/project.service'
import { CommentApplicationService } from '@/services/application/comment.service'

export interface Services {
  label: LabelApplicationService,
  member: MemberApplicationService,
  user: UserApplicationService,
  role: RoleApplicationService,
  project: ProjectApplicationService,
  comment: CommentApplicationService
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
  const userRepository = new FromApiUserItemListRepository()
  const user = new UserApplicationService(userRepository)
  const roleRepository = new FromApiRoleItemListRepository()
  const role = new RoleApplicationService(roleRepository)
  const projectRepository = new FromApiProjectItemListRepository()
  const project = new ProjectApplicationService(projectRepository)
  const commentRepository = new FromApiCommentItemListRepository()
  const comment = new CommentApplicationService(commentRepository)
  const services: Services = {
    label,
    member,
    user,
    role,
    project,
    comment
  }
  inject('services', services)
}

export default plugin
