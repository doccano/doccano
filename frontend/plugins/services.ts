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
import { FromApiSeq2seqRepository } from '@/repositories/tasks/seq2seq/api'
import { Seq2seqApplicationService } from '@/services/application/tasks/seq2seqService'
import { ConfigApplicationService } from '@/services/application/config.service'
import { FromApiConfigItemListRepository } from '@/repositories/config/api'
import { TemplateApplicationService } from '@/services/application/template.service'
import { FromApiTemplateRepository } from '@/repositories/template/api'
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
  seq2seq: Seq2seqApplicationService,
  option: OptionApplicationService,
  config: ConfigApplicationService,
  template: TemplateApplicationService
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
  const seq2seqRepository = new FromApiSeq2seqRepository()
  const optionRepository     = new LocalStorageOptionRepository()
  const configRepository     = new FromApiConfigItemListRepository()
  const templateRepository   = new FromApiTemplateRepository()

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
  const seq2seq = new Seq2seqApplicationService(seq2seqRepository)
  const option = new OptionApplicationService(optionRepository)
  const config = new ConfigApplicationService(configRepository)
  const template = new TemplateApplicationService(templateRepository)
  
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
    seq2seq,
    option,
    config,
    template
  }
  inject('services', services)
}

export default plugin
