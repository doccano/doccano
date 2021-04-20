import { Plugin } from '@nuxt/types'
import { APISequenceLabelingRepository } from '~/repositories/tasks/sequenceLabeling/apiSequenceLabeling'
import { APISeq2seqRepository } from '~/repositories/tasks/seq2seq/apiSeq2seq'
import { APIConfigRepository } from '~/repositories/autoLabeling/config/apiConfigRepository'
import { APITemplateRepository } from '~/repositories/autoLabeling/template/apiTemplateRepository'
import { APIUserRepository } from '~/repositories/user/apiUserRepository'
import { APIStatisticsRepository } from '~/repositories/statistics/apiStatisticsRepository'
import { APIRoleRepository } from '~/repositories/role/apiRoleRepository'
import { APIProjectRepository } from '~/repositories/project/apiProjectRepository'
import { LocalStorageOptionRepository} from '~/repositories/option/apiOptionRepository'
import { APIMemberRepository } from '~/repositories/member/apiMemberRepository'
import { APILabelRepository } from '~/repositories/label/apiLabelRepository'
import { APIDocumentRepository } from '~/repositories/document/apiDocumentRepository'
import { APICommentRepository } from '~/repositories/comment/apiCommentRepository'
import { APIAuthRepository } from '~/repositories/auth/apiAuthRepository'
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
import { APITextClassificationRepository } from '~/repositories/tasks/textClassification/apiTextClassification'
import { TextClassificationApplicationService } from '~/services/application/tasks/textClassification/textClassificationApplicationService'
import { AuthApplicationService } from '~/services/application/auth/authApplicationService'

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
  template: TemplateApplicationService,
  auth: AuthApplicationService
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $services: Services
  }
}

const plugin: Plugin = (context, inject) => {
  const labelRepository      = new APILabelRepository()
  const memberRepository     = new APIMemberRepository()
  const userRepository       = new APIUserRepository()
  const roleRepository       = new APIRoleRepository()
  const projectRepository    = new APIProjectRepository()
  const commentRepository    = new APICommentRepository()
  const statisticsRepository = new APIStatisticsRepository()
  const documentRepository   = new APIDocumentRepository()
  const textClassificationRepository = new APITextClassificationRepository()
  const sequenceLabelingRepository   = new APISequenceLabelingRepository()
  const seq2seqRepository = new APISeq2seqRepository()
  const optionRepository     = new LocalStorageOptionRepository()
  const configRepository     = new APIConfigRepository()
  const templateRepository   = new APITemplateRepository()
  const authRepository = new APIAuthRepository()

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
  const auth = new AuthApplicationService(authRepository)
  
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
    template,
    auth
  }
  inject('services', services)
}

export default plugin
