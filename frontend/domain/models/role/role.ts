export type RoleName = 'project_admin' | 'annotator' | 'annotation_approver'

export class RoleItem {
  constructor(readonly id: number, readonly name: RoleName) {}
}
