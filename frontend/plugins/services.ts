import { Plugin } from '@nuxt/types'
import { APITaskStatusRepository } from '@/repositories/celery/apiTaskStatusRepository'
import { TaskStatusApplicationService } from '@/services/application/celery/taskStatusApplicationService'
import { APICatalogRepository } from '../repositories/upload/apiCatalogRepository'
import { CatalogApplicationService } from '../services/application/upload/catalogApplicationService'
import { APIParseRepository } from '../repositories/upload/apiParseRepository'
import { ParseApplicationService } from '../services/application/upload/parseApplicationService'
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
import { APIExampleRepository } from '~/repositories/example/apiDocumentRepository'
import { APICommentRepository } from '~/repositories/comment/apiCommentRepository'
import { APIAuthRepository } from '~/repositories/auth/apiAuthRepository'
import { LabelApplicationService } from '~/services/application/label/labelApplicationService'
import { MemberApplicationService } from '~/services/application/member/memberApplicationService'
import { UserApplicationService } from '~/services/application/user/userApplicationService'
import { RoleApplicationService } from '~/services/application/role/roleApplicationService'
import { ProjectApplicationService } from '~/services/application/project/projectApplicationService'
import { CommentApplicationService } from '~/services/application/comment/commentApplicationService'
import { StatisticsApplicationService } from '~/services/application/statistics/statisticsApplicationService'
import { ExampleApplicationService } from '~/services/application/example/exampleApplicationService'
import { OptionApplicationService } from '~/services/application/option/optionApplicationService'
import { SequenceLabelingApplicationService } from '~/services/application/tasks/sequenceLabeling/sequenceLabelingApplicationService'
import { Seq2seqApplicationService } from '~/services/application/tasks/seq2seq/seq2seqApplicationService'
import { ConfigApplicationService } from '~/services/application/autoLabeling/configApplicationService'
import { TemplateApplicationService } from '~/services/application/autoLabeling/templateApplicationService'
import { APITextClassificationRepository } from '~/repositories/tasks/textClassification/apiTextClassification'
import { TextClassificationApplicationService } from '~/services/application/tasks/textClassification/textClassificationApplicationService'
import { AuthApplicationService } from '~/services/application/auth/authApplicationService'
import { APIDownloadFormatRepository } from '~/repositories/download/apiDownloadFormatRepository'
import { APIDownloadRepository } from '~/repositories/download/apiDownloadRepository'
import { DownloadApplicationService } from '~/services/application/download/downloadApplicationService'
import { DownloadFormatApplicationService } from '~/services/application/download/downloadFormatApplicationService'
import { APITagRepository } from '~/repositories/tag/apiTagRepository'
import { TagApplicationService } from '~/services/application/tag/tagApplicationService'
import {ApiLinkRepository} from "~/repositories/links/apiLinkRepository";
import {LinkTypesApplicationService} from "~/services/application/links/linkTypesApplicationService";
import {ApiLinkTypesRepository} from "~/repositories/links/apiLinkTypesRepository";

export interface Services {
  label: LabelApplicationService,
  linkTypes: LinkTypesApplicationService,
  member: MemberApplicationService,
  user: UserApplicationService,
  role: RoleApplicationService,
  project: ProjectApplicationService,
  comment: CommentApplicationService,
  statistics: StatisticsApplicationService,
  example: ExampleApplicationService,
  textClassification: TextClassificationApplicationService,
  sequenceLabeling: SequenceLabelingApplicationService,
  seq2seq: Seq2seqApplicationService,
  option: OptionApplicationService,
  config: ConfigApplicationService,
  template: TemplateApplicationService,
  auth: AuthApplicationService,
  catalog: CatalogApplicationService,
  parse: ParseApplicationService,
  taskStatus: TaskStatusApplicationService,
  downloadFormat: DownloadFormatApplicationService,
  download: DownloadApplicationService,
  tag: TagApplicationService,
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $services: Services
  }
}

const plugin: Plugin = (context, inject) => {
  const labelRepository      = new APILabelRepository()
  const linkTypesRepository = new ApiLinkTypesRepository()
  const memberRepository     = new APIMemberRepository()
  const userRepository       = new APIUserRepository()
  const roleRepository       = new APIRoleRepository()
  const projectRepository    = new APIProjectRepository()
  const commentRepository    = new APICommentRepository()
  const statisticsRepository = new APIStatisticsRepository()
  const exampleRepository    = new APIExampleRepository()
  const textClassificationRepository = new APITextClassificationRepository()
  const sequenceLabelingRepository   = new APISequenceLabelingRepository()
  const linkRepository = new ApiLinkRepository()
  const seq2seqRepository = new APISeq2seqRepository()
  const optionRepository     = new LocalStorageOptionRepository()
  const configRepository     = new APIConfigRepository()
  const tagRepository = new APITagRepository()
  const templateRepository   = new APITemplateRepository()
  const authRepository = new APIAuthRepository()
  const catalogRepository = new APICatalogRepository()
  const parseRepository = new APIParseRepository()
  const taskStatusRepository = new APITaskStatusRepository()
  const downloadFormatRepository = new APIDownloadFormatRepository()
  const downloadRepository = new APIDownloadRepository()

  const label      = new LabelApplicationService(labelRepository)
  const linkTypes = new LinkTypesApplicationService(linkTypesRepository)
  const member     = new MemberApplicationService(memberRepository)
  const user       = new UserApplicationService(userRepository)
  const role       = new RoleApplicationService(roleRepository)
  const project    = new ProjectApplicationService(projectRepository)
  const comment    = new CommentApplicationService(commentRepository)
  const statistics = new StatisticsApplicationService(statisticsRepository)
  const example    = new ExampleApplicationService(exampleRepository)
  const textClassification = new TextClassificationApplicationService(textClassificationRepository)
  const sequenceLabeling   = new SequenceLabelingApplicationService(sequenceLabelingRepository, linkRepository)
  const seq2seq = new Seq2seqApplicationService(seq2seqRepository)
  const option = new OptionApplicationService(optionRepository)
  const config = new ConfigApplicationService(configRepository)
  const tag = new TagApplicationService(tagRepository)
  const template = new TemplateApplicationService(templateRepository)
  const auth = new AuthApplicationService(authRepository)
  const catalog = new CatalogApplicationService(catalogRepository)
  const parse = new ParseApplicationService(parseRepository)
  const taskStatus = new TaskStatusApplicationService(taskStatusRepository)
  const downloadFormat = new DownloadFormatApplicationService(downloadFormatRepository)
  const download = new DownloadApplicationService(downloadRepository)
  
  const services: Services = {
    label,
    linkTypes,
    member,
    user,
    role,
    project,
    comment,
    statistics,
    example,
    textClassification,
    sequenceLabeling,
    seq2seq,
    option,
    config,
    template,
    auth,
    catalog,
    parse,
    taskStatus,
    downloadFormat,
    download,
    tag,
  }
  inject('services', services)
}

export default plugin
