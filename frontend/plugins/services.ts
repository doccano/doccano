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
import { FromApiSequenceLabelingRepository } from '@/repositories/tasks/sequenceLabeling/api'
import { FromApiSeq2seqRepository } from '@/repositories/tasks/seq2seq/api'
import { FromApiConfigItemListRepository } from '@/repositories/config/api'
import { FromApiTemplateRepository } from '@/repositories/template/api'
import { LabelApplicationService } from '~/services/application/label/labelApplicationService'
import { MemberApplicationService } from '~/services/application/member/memberApplicationService'
import { UserApplicationService } from '~/services/application/user/userApplicationService'
import { RoleApplicationService } from '~/services/application/role/roleApplicationService'
import { ProjectApplicationService } from '~/services/application/project/projectApplicationService'
import { CommentApplicationService } from '~/services/application/comment/commentApplicationService'
import { StatisticsApplicationService } from '~/services/application/statistics/statisticsApplicationService'
import { DocumentApplicationService } from '~/services/application/document/documentApplicationService'
import { OptionApplicationService } from '~/services/application/option/optionApplicationService'
import { SequenceLabelingApplicationService } from '~/services/application/tasks/sequenceLabeling/sequenceLabelingApplicationService'
import { Seq2seqApplicationService } from '~/services/application/tasks/seq2seq/seq2seqApplicationService'
import { ConfigApplicationService } from '~/services/application/autoLabeling/configApplicationService'
import { TemplateApplicationService } from '~/services/application/autoLabeling/templateApplicationService'
import { FromApiTextClassificationRepository } from '~/repositories/tasks/textClassification/api'
import { TextClassificationApplicationService } from '~/services/application/tasks/textClassification/textClassificationApplicationService'


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
