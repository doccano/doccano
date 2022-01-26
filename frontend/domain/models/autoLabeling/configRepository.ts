import { ConfigItem, ConfigItemList } from '~/domain/models/autoLabeling/config'

export interface ConfigTestResponse {
  valid: boolean,
  labels: object[]
}

export interface ConfigRepository {
  list(projectId: string): Promise<ConfigItemList>

  create(projectId: string, item: ConfigItem): Promise<ConfigItem>

  delete(projectId: string, itemId: number): Promise<void>

  update(projectId: string, item: ConfigItem): Promise<ConfigItem>

  testParameters(projectId: string, item: ConfigItem, text: string): Promise<ConfigTestResponse>

  testTemplate(projectId: string, response: any, item: ConfigItem): Promise<ConfigTestResponse>

  testMapping(projectId: string, item: ConfigItem, response: any): Promise<ConfigTestResponse>
}
