export default {
  colorRules: {
    colorRequired: 'Color is required'
  },
  labelNameRules: {
    labelRequired: 'Label name is required',
    labelLessThan100Chars: 'Label name must be less than 100 characters',
    duplicated: 'The label name is already used.'
  },
  keyNameRules: {
    duplicated: 'The key is already used.'
  },
  userNameRules: {
    userNameRequired: 'User name is required',
    userNameLessThan30Chars: 'User name must be less than 30 characters'
  },
  roleRules: {
    roleRequired: 'Role is required'
  },
  projectName: {
    required: 'Project name is required',
    maxLength: 'Project name must be less than 100 characters'
  },
  description: {
    required: 'Description is required'
  },
  fileFormatRules: {
    fileFormatRequired: 'File format is required'
  },
  uploadFileRules: {
    fileRequired: 'File is required',
    fileLessThan1MB: 'File size should be less than 100 MB!'
  },
  passwordRules: {
    passwordRequired: 'Password is required',
    passwordLessThan30Chars: 'Password must be less than 30 characters'
  }
}
