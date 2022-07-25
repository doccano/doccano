import { Plugin } from '@nuxt/types'
import { TaskStatusApplicationService } from '@/services/application/celery/taskStatusApplicationService'
import { CatalogApplicationService } from '@/services/application/upload/catalogApplicationService'
import { ParseApplicationService } from '@/services/application/upload/parseApplicationService'
import { LabelApplicationService } from '@/services/application/label/labelApplicationService'
import { MemberApplicationService } from '@/services/application/member/memberApplicationService'
import { UserApplicationService } from '@/services/application/user/userApplicationService'
import { RoleApplicationService } from '@/services/application/role/roleApplicationService'
import { ProjectApplicationService } from '@/services/application/project/projectApplicationService'
import { CommentApplicationService } from '@/services/application/comment/commentApplicationService'
import { MetricsApplicationService } from '@/services/application/metrics/metricsApplicationService'
import { ExampleApplicationService } from '@/services/application/example/exampleApplicationService'
import { OptionApplicationService } from '@/services/application/option/optionApplicationService'
import { SequenceLabelingApplicationService } from '@/services/application/tasks/sequenceLabeling/sequenceLabelingApplicationService'
import { Seq2seqApplicationService } from '@/services/application/tasks/seq2seq/seq2seqApplicationService'
import { ConfigApplicationService } from '@/services/application/autoLabeling/configApplicationService'
import { TemplateApplicationService } from '@/services/application/autoLabeling/templateApplicationService'
import { TextClassificationService } from '@/services/application/tasks/textClassification/textClassificationApplicationService'
import { AuthApplicationService } from '@/services/application/auth/authApplicationService'
import { DownloadApplicationService } from '@/services/application/download/downloadApplicationService'
import { DownloadFormatApplicationService } from '@/services/application/download/downloadFormatApplicationService'
import { TagApplicationService } from '@/services/application/tag/tagApplicationService'
import { BoundingBoxApplicationService } from '@/services/application/tasks/boundingBox/boundingBoxApplicationService'
import { SegmentationApplicationService } from '@/services/application/tasks/segmentation/segmentationApplicationService'
import { repositories } from './repositories'

export interface Services {
  categoryType: LabelApplicationService
  spanType: LabelApplicationService
  relationType: LabelApplicationService
  member: MemberApplicationService
  user: UserApplicationService
  role: RoleApplicationService
  project: ProjectApplicationService
  comment: CommentApplicationService
  metrics: MetricsApplicationService
  example: ExampleApplicationService
  textClassification: TextClassificationService
  sequenceLabeling: SequenceLabelingApplicationService
  seq2seq: Seq2seqApplicationService
  option: OptionApplicationService
  config: ConfigApplicationService
  template: TemplateApplicationService
  auth: AuthApplicationService
  catalog: CatalogApplicationService
  parse: ParseApplicationService
  taskStatus: TaskStatusApplicationService
  downloadFormat: DownloadFormatApplicationService
  download: DownloadApplicationService
  tag: TagApplicationService
  bbox: BoundingBoxApplicationService
  segmentation: SegmentationApplicationService
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $services: Services
  }
}

const plugin: Plugin = (_, inject) => {
  const services: Services = {
    categoryType: new LabelApplicationService(repositories.categoryType),
    spanType: new LabelApplicationService(repositories.spanType),
    relationType: new LabelApplicationService(repositories.relationType),
    member: new MemberApplicationService(repositories.member),
    user: new UserApplicationService(repositories.user),
    role: new RoleApplicationService(repositories.role),
    project: new ProjectApplicationService(repositories.project),
    comment: new CommentApplicationService(repositories.comment),
    metrics: new MetricsApplicationService(repositories.metrics),
    example: new ExampleApplicationService(repositories.example),
    textClassification: new TextClassificationService(repositories.category),
    sequenceLabeling: new SequenceLabelingApplicationService(
      repositories.span,
      repositories.relation
    ),
    seq2seq: new Seq2seqApplicationService(repositories.textLabel),
    option: new OptionApplicationService(repositories.option),
    config: new ConfigApplicationService(repositories.config),
    template: new TemplateApplicationService(repositories.template),
    auth: new AuthApplicationService(repositories.auth),
    catalog: new CatalogApplicationService(repositories.catalog),
    parse: new ParseApplicationService(repositories.parse),
    taskStatus: new TaskStatusApplicationService(repositories.taskStatus),
    downloadFormat: new DownloadFormatApplicationService(repositories.downloadFormat),
    download: new DownloadApplicationService(repositories.download),
    tag: new TagApplicationService(repositories.tag),
    bbox: new BoundingBoxApplicationService(repositories.boundingBox),
    segmentation: new SegmentationApplicationService(repositories.segmentation)
  }
  inject('services', services)
}

export default plugin
