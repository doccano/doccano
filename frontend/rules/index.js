// Rules for project label.
export const colorRules = (msg) => {
  return [(v) => !!v || msg.colorRequired]
}

export const labelNameRules = (msg) => {
  return [(v) => !!v || msg.labelRequired, (v) => (v && v.length <= 30) || msg.labelLessThan30Chars]
}

// Rules for project member.
export const userNameRules = (msg) => {
  return [
    (v) => !!v || msg.userNameRequired,
    (v) => (v && v.length <= 30) || msg.userNameLessThan30Chars,
    (v) => (v && v.length >= 3) || msg.minLength
  ]
}

export const roleRules = (msg) => {
  return [(v) => !!v || msg.roleRequired]
}

// Rules for Document.
export const fileFormatRules = (msg) => {
  return [(v) => !!v || msg.fileFormatRequired]
}

export const uploadFileRules = (msg) => {
  return [
    (v) => !!v || msg.fileRequired,
    (v) => !v || v.some((file) => file.size < 100000000) || msg.fileLessThan1MB
  ]
}

export const uploadSingleFileRules = (msg) => {
  return [(v) => !!v || msg.fileRequired, (v) => !v || v.size < 1000000 || msg.fileLessThan1MB]
}

// Rules for user.
export const passwordRules = (msg) => {
  return [
    (v) => !!v || msg.passwordRequired,
    (v) => (v && v.length <= 30) || msg.passwordLessThan30Chars,
    (v) => (v && v.length >= 8) || msg.minLength,
  ]
}

export const templateNameRules = () => {
  return [(v) => !!v || 'Name is required']
}

export const emailRules = (msg) => {
  return [
    (v) => !!v || msg.required,
    (v) => {
      const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
      return pattern.test(v) || msg.format
    }
  ]
}
