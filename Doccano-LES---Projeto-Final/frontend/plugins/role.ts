import Vue from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $translateRole(role: string, mappings: object): string
  }
}

type RoleMapping = {
  projectAdmin: string
  annotator: string
  annotationApprover: string
  undefined: string
}

Vue.prototype.$translateRole = (role: string, mapping: RoleMapping) => {
  if (role === 'project_admin') {
    return mapping.projectAdmin
  } else if (role === 'annotator') {
    return mapping.annotator
  } else if (role === 'annotation_approver') {
    return mapping.annotationApprover
  } else {
    return mapping.undefined
  }
}
