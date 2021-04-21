export class ConfigItemList {
  constructor(public configItems: ConfigItem[]) {}

  static valueOf(items: ConfigItem[]): ConfigItemList {
    return new ConfigItemList(items)
  }

  toArray(): Object[] {
    return this.configItems.map(item => item.toObject())
  }
}

interface LabelMappingForUI {
  from: string,
  to: string
}

export interface ParametersForUI {
  name: string,
  value: string | object[],
  type?: string,
  items?: string[]
}

export interface Fields {
  modelName: string,
  modelAttrs: ParametersForUI[],
  template: string,
  labelMapping: LabelMappingForUI[]
}

export class ConfigItem {
  constructor(
    public id: number,
    public modelName: string,
    public modelAttrs: object,
    public template: string,
    public labelMapping: object
  ) {}

  static valueOf(
    { id, model_name, model_attrs, template, label_mapping }:
    { id: number, model_name: string, model_attrs: object, template: string, label_mapping: object }
  ): ConfigItem {
    return new ConfigItem(id, model_name, model_attrs, template, label_mapping)
  }

  static parseFromUI(
    { modelName, modelAttrs, template, labelMapping }: Fields): ConfigItem {
    const mapping = labelMapping.reduce((a, x) => ({...a, [x.from]: x.to}), {})
    const attributes: {[key: string]: any} = modelAttrs.reduce((a, x) => ({...a, [x.name]: x.value}), {})
    for (const [key, value] of Object.entries(attributes)) {
      if (Array.isArray(value)) {
        attributes[key] = value.reduce((a, x) => ({...a, [x.key]: x.value}), {})
      }
    }
    return new ConfigItem(99999, modelName, attributes, template, mapping)
  }

  toObject(): object {
    return {
      id: this.id,
      modelName: this.modelName,
      modelAttrs: this.modelAttrs,
      template: this.template,
      labelMapping: this.labelMapping
    }
  }

  toAPI(): object {
    return {
      id: this.id,
      model_name: this.modelName,
      model_attrs: this.modelAttrs,
      template: this.template,
      label_mapping: this.labelMapping
    }
  }
}
