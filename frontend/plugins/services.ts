import { Plugin } from '@nuxt/types'
import { FromApiLabelItemListRepository } from '@/repositories/label/api'
import { FromApiMemberItemListRepository } from '@/repositories/member/api'
import { FromApiUserItemListRepository } from '@/repositories/user/api'
import { FromApiRoleItemListRepository } from '@/repositories/role/api'
import { FromApiProjectItemListRepository } from '@/repositories/project/api'
import { FromApiCommentItemListRepository } from '@/repositories/comment/api'
import { FromApiStatisticsRepository } from '@/repositories/statistics/api'
import { FromApiDocumentItemListRepository } from '@/repositories/document/api'
import { LocalStorageOptionRepository} from '@/repositories/option/api'
import { LabelApplicationService } from '@/services/application/label.service'
import { MemberApplicationService } from '@/services/application/member.service'
import { UserApplicationService } from '@/services/application/user.service'
import { RoleApplicationService } from '@/services/application/role.service'
import { ProjectApplicationService } from '@/services/application/project.service'
import { CommentApplicationService } from '@/services/application/comment.service'
import { StatisticsApplicationService } from '@/services/application/statistics.service'
import { DocumentApplicationService } from '@/services/application/document.service'
import { OptionApplicationService } from '@/services/application/option.service'
import { FromApiSequenceLabelingRepository } from '@/repositories/tasks/sequenceLabeling/api'
import { SequenceLabelingApplicationService } from '@/services/application/tasks/sequenceLabelingService'
import { FromApiTextClassificationRepository } from '~/repositories/tasks/textClassification/api'
import { TextClassificationApplicationService } from '~/services/application/tasks/textClassificationService'



export interface Services {
  label: LabelApplicationService,
  member: MemberApplicationService,
  user: UserApplicationService,
  role: RoleApplicationService,
  project: ProjectApplicationService,
  comment: CommentApplicationService,
  statistics: StatisticsApplicationService,
  document: DocumentApplicationService,
  textClassification: TextClassificationApplicationService,
  sequenceLabeling: SequenceLabelingApplicationService,
  option: OptionApplicationService
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $services: Services
  }
}

const plugin: Plugin = (context, inject) => {
  const labelRepository      = new FromApiLabelItemListRepository()
  const memberRepository     = new FromApiMemberItemListRepository()
  const userRepository       = new FromApiUserItemListRepository()
  const roleRepository       = new FromApiRoleItemListRepository()
  const projectRepository    = new FromApiProjectItemListRepository()
  const commentRepository    = new FromApiCommentItemListRepository()
  const statisticsRepository = new FromApiStatisticsRepository()
  const documentRepository   = new FromApiDocumentItemListRepository()
  const textClassificationRepository = new FromApiTextClassificationRepository()
  const sequenceLabelingRepository   = new FromApiSequenceLabelingRepository()
  const optionRepository     = new LocalStorageOptionRepository()

  const label      = new LabelApplicationService(labelRepository)
  const member     = new MemberApplicationService(memberRepository)
  const user       = new UserApplicationService(userRepository)
  const role       = new RoleApplicationService(roleRepository)
  const project    = new ProjectApplicationService(projectRepository)
  const comment    = new CommentApplicationService(commentRepository)
  const statistics = new StatisticsApplicationService(statisticsRepository)
  const document   = new DocumentApplicationService(documentRepository)
  const textClassification = new TextClassificationApplicationService(textClassificationRepository)
  const sequenceLabeling   = new SequenceLabelingApplicationService(sequenceLabelingRepository)
  const option = new OptionApplicationService(optionRepository)
  
  const services: Services = {
    label,
    member,
    user,
    role,
    project,
    comment,
    statistics,
    document,
    textClassification,
    sequenceLabeling,
    option
  }
  inject('services', services)
}

export default plugin
