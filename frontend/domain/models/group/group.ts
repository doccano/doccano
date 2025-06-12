export class Group {
  constructor(
    public id: number,
    public name: string
  ) {}
}

export class GroupDetails extends Group {
  constructor(
    public id: number,
    public name: string,
    public permissions?: number[],
    public permission_names?: {[key: string]: {
      name: string;
      codename: string;
      content_type: string;
    }}
  ) {
    super(id, name);
  }
}

export class Permission {
  constructor(
    public id: number,
    public name: string,
    public codename: string,
    public content_type?: number,
    public label?: string
  ) {}
}

export class ContentType {
  constructor(
    public id: number,
    public app_label: string,
    public model: string
  ) {}
}
