import { Fields, ParametersForUI } from '~/domain/models/autoLabeling/config'

export interface Schema {
  title: string
  type: string
  properties: object
}

export interface ConfigResponse {
  name: string
  schema: Schema
  template: string
}

export class ConfigTemplateItem {
  constructor(private schema: Schema, public template: string) {}

  static valueOf({ schema, template }: { schema: Schema; template: string }): ConfigTemplateItem {
    return new ConfigTemplateItem(schema, template)
  }

  get modelName(): string {
    return this.schema.title
  }

  get fields(): ParametersForUI[] {
    const response: ParametersForUI[] = []
    for (const [key, value] of Object.entries(this.schema.properties)) {
      if ('type' in value && value.type === 'string') {
        response.push({ name: key, type: 'textField', value: '' })
      } else if ('anyOf' in value) {
        response.push({
          name: key,
          type: 'selectField',
          value: '',
          items: value.anyOf.map((item: { const: string; type: string }) => item.const)
        })
      } else if ('type' in value && value.type === 'object') {
        response.push({
          name: key,
          type: 'objectField',
          value: []
        })
      }
    }
    return response
  }

  toObject(): Fields {
    return {
      modelName: this.modelName,
      template: this.template,
      modelAttrs: this.fields,
      labelMapping: [],
      taskType: ''
    }
  }
}
