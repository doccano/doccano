// Rules for project label.
export const colorRules = (msg) => {
  return [
    v => !!v || msg.rule1
  ]
}

export const labelNameRules = (msg) => {
  return [
    v => !!v || msg.rule1,
    v => (v && v.length <= 30) || msg.rule2
  ]
}

// Rules for project member.
export const userNameRules = (msg) => {
  return [
    v => !!v || msg.rule1,
    v => (v && v.length <= 30) || msg.rule2
  ]
}

export const roleRules = (msg) => {
  return [
    v => !!v || msg.rule1
  ]
}

// Rules for a project.
export const projectNameRules = (msg) => {
  return [
    v => !!v || msg.rule1,
    v => (v && v.length <= 30) || msg.rule2
  ]
}

export const descriptionRules = (msg) => {
  return [
    v => !!v || msg.rule1,
    v => (v && v.length <= 100) || msg.rule2
  ]
}

export const projectTypeRules = (msg) => {
  return [
    v => !!v || msg.rule1
  ]
}

// Rules for Document.
export const fileFormatRules = (msg) => {
  return [
    v => !!v || msg.rule1
  ]
}

export const uploadFileRules = (msg) => {
  return [
    v => !!v || msg.rule1,
    v => !v || v.size < 1000000 || msg.rule2
  ]
}

// Rules for user.
export const passwordRules = (msg) => {
  return [
    v => !!v || msg.rule1,
    v => (v && v.length <= 30) || msg.rule2
  ]
}
