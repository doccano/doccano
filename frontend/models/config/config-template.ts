export interface Schema {
  title: string,
  type: string,
  properties: object
}

export interface ConfigResponse {
  name: string,
  schema: Schema,
  template: string
}

export class ConfigTemplateItem {
  constructor(
    private schema: Schema,
    public template: string
  ) {}

  static valueOf(
    { schema, template }:
    { schema: Schema, template: string }
  ): ConfigTemplateItem {
    return new ConfigTemplateItem(schema, template)
  }

  get modelName(): string {
    return this.schema.title
  }

  get fields() {
    const response = []
    for (const [key, value] of Object.entries(this.schema.properties)) {
      if ('type' in value && value.type === 'string') {
        response.push({name: key, type: 'textField', value: ''})
      } else if ('anyOf' in value) {
        response.push(
          {
            name: key,
            type: 'selectField',
            value: '',
            items: value['anyOf'].map(
              (item: {'const': string, 'type': string}) => item.const
            )
          }
        )
      } else if ('type' in value && value.type === 'object') {
        response.push(
          {
            name: key,
            type: 'objectField',
            value: []
          }
        )
      }
    }
    return response
  }

  toObject(): Object {
    return {
      model_name: this.modelName,
      template: this.template,
      model_attrs: this.fields
    }
  }
}

export const headers = [
  {
    text: 'From',
    align: 'left',
    value: 'from',
    sortable: false
  },
  {
    text: 'To',
    align: 'left',
    value: 'to',
    sortable: false
  },
  {
    text: 'Actions',
    value: 'actions',
    sortable: false
  }
]
