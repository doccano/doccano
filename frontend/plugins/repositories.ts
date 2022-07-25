import { Plugin } from '@nuxt/types'
import { APITaskStatusRepository } from '@/repositories/celery/apiTaskStatusRepository'
import { APICatalogRepository } from '@/repositories/upload/apiCatalogRepository'
import { APIParseRepository } from '@/repositories/upload/apiParseRepository'
import { APISequenceLabelingRepository } from '@/repositories/tasks/sequenceLabeling/apiSequenceLabeling'
import { APISeq2seqRepository } from '@/repositories/tasks/seq2seq/apiSeq2seq'
import { APIConfigRepository } from '@/repositories/autoLabeling/config/apiConfigRepository'
import { APITemplateRepository } from '@/repositories/autoLabeling/template/apiTemplateRepository'
import { APIUserRepository } from '@/repositories/user/apiUserRepository'
import { APIMetricsRepository } from '@/repositories/metrics/apiMetricsRepository'
import { APIRoleRepository } from '@/repositories/role/apiRoleRepository'
import { APIProjectRepository } from '@/repositories/project/apiProjectRepository'
import { LocalStorageOptionRepository } from '@/repositories/option/apiOptionRepository'
import { APIMemberRepository } from '@/repositories/member/apiMemberRepository'
import { APILabelRepository } from '@/repositories/label/apiLabelRepository'
import { APIExampleRepository } from '@/repositories/example/apiDocumentRepository'
import { APICommentRepository } from '@/repositories/comment/apiCommentRepository'
import { APIAuthRepository } from '@/repositories/auth/apiAuthRepository'
import { APITextClassificationRepository } from '@/repositories/tasks/textClassification/apiTextClassification'
import { APIDownloadFormatRepository } from '@/repositories/download/apiDownloadFormatRepository'
import { APIDownloadRepository } from '@/repositories/download/apiDownloadRepository'
import { APITagRepository } from '@/repositories/tag/apiTagRepository'
import { ApiRelationRepository } from '@/repositories/tasks/sequenceLabeling/apiRelationRepository'
import { ApiBoundingBoxRepository } from '@/repositories/tasks/boundingBox/apiBoundingBoxRepository'
import { ApiSegmentationRepository } from '@/repositories/tasks/segmentation/apiSegmentationRepository'

export interface Repositories {
  // User
  auth: APIAuthRepository
  user: APIUserRepository

  // Project
  project: APIProjectRepository
  member: APIMemberRepository
  role: APIRoleRepository
  tag: APITagRepository

  // Example
  example: APIExampleRepository
  comment: APICommentRepository
  taskStatus: APITaskStatusRepository
  metrics: APIMetricsRepository
  option: LocalStorageOptionRepository

  // Auto Labeling
  config: APIConfigRepository
  template: APITemplateRepository

  // Upload
  catalog: APICatalogRepository
  parse: APIParseRepository

  // Download
  downloadFormat: APIDownloadFormatRepository
  download: APIDownloadRepository

  // Label Type
  categoryType: APILabelRepository
  spanType: APILabelRepository
  relationType: APILabelRepository

  // Label
  category: APITextClassificationRepository
  span: APISequenceLabelingRepository
  relation: ApiRelationRepository
  textLabel: APISeq2seqRepository
  boundingBox: ApiBoundingBoxRepository
  segmentation: ApiSegmentationRepository
}

declare module 'vue/types/vue' {
  interface Vue {
    readonly $repositories: Repositories
  }
}

const repositories: Repositories = {
  // User
  auth: new APIAuthRepository(),
  user: new APIUserRepository(),

  // Project
  project: new APIProjectRepository(),
  member: new APIMemberRepository(),
  role: new APIRoleRepository(),
  tag: new APITagRepository(),

  // Example
  example: new APIExampleRepository(),
  comment: new APICommentRepository(),
  taskStatus: new APITaskStatusRepository(),
  metrics: new APIMetricsRepository(),
  option: new LocalStorageOptionRepository(),

  // Auto Labeling
  config: new APIConfigRepository(),
  template: new APITemplateRepository(),

  // Upload
  catalog: new APICatalogRepository(),
  parse: new APIParseRepository(),

  // Download
  downloadFormat: new APIDownloadFormatRepository(),
  download: new APIDownloadRepository(),

  // Label Type
  categoryType: new APILabelRepository('category-type'),
  spanType: new APILabelRepository('span-type'),
  relationType: new APILabelRepository('relation-type'),

  // Label
  category: new APITextClassificationRepository(),
  span: new APISequenceLabelingRepository(),
  relation: new ApiRelationRepository(),
  textLabel: new APISeq2seqRepository(),
  boundingBox: new ApiBoundingBoxRepository(),
  segmentation: new ApiSegmentationRepository()
}

const plugin: Plugin = (_, inject) => {
  inject('repositories', repositories)
}

export default plugin
export { repositories }
