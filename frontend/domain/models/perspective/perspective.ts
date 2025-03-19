import { PerspectiveAttributeItem } from "./perspectiveAttribute";

export class PerspectiveItem {
  constructor(
    readonly id: number,
    readonly name: string,
    readonly description: string,
    readonly attributes: PerspectiveAttributeItem[] = [],
  ) {}

  static create(
    id: number,
    name: string,
    description: string,
    attributes: PerspectiveAttributeItem[],
  ): PerspectiveItem {
    return new PerspectiveItem(id, name, description, attributes);
  }
}