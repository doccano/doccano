export class PerspectiveAttributeItem {
    constructor(
      readonly id: number,
      readonly perspectiveId: number,
      readonly name: string,
      readonly description: string
    ) {}
  
    static create(
      id: number,
      perspectiveId: number,
      name: string,
      description: string
    ): PerspectiveAttributeItem {
      return new PerspectiveAttributeItem(id, perspectiveId, name, description);
    }
  }