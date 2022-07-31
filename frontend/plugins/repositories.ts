import { Plugin } from '@nuxt/types'
import { APITaskStatusRepository } from '@/repositories/celery/apiTaskStatusRepository'
import { APICatalogRepository } from '@/repositories/upload/apiCatalogRepository'
import { APIParseRepository } from '@/repositories/upload/apiParseRepository'
import { APISpanRepository } from '@/repositories/tasks/apiSpanRepository'
import { APITextLabelRepository } from '@/repositories/tasks/apiTextLabelRepository'
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
import { APICategoryRepository } from '@/repositories/tasks/apiCategoryRepository'
import { APIDownloadFormatRepository } from '@/repositories/download/apiDownloadFormatRepository'
import { APIDownloadRepository } from '@/repositories/download/apiDownloadRepository'
import { APITagRepository } from '@/repositories/tag/apiTagRepository'
import { APIRelationRepository } from '@/repositories/tasks/apiRelationRepository'
import { APIBoundingBoxRepository } from '@/repositories/tasks/apiBoundingBoxRepository'
import { APISegmentationRepository } from '~/repositories/tasks/apiSegmentationRepository'

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
  category: APICategoryRepository
  span: APISpanRepository
  relation: APIRelationRepository
  textLabel: APITextLabelRepository
  boundingBox: APIBoundingBoxRepository
  segmentation: APISegmentationRepository
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
  category: new APICategoryRepository(),
  span: new APISpanRepository(),
  relation: new APIRelationRepository(),
  textLabel: new APITextLabelRepository(),
  boundingBox: new APIBoundingBoxRepository(),
  segmentation: new APISegmentationRepository()
}

const plugin: Plugin = (_, inject) => {
  inject('repositories', repositories)
}

export default plugin
export { repositories }
