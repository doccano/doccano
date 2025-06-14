export default {
  colorRules: {
    colorRequired: '请输入颜色'
  },
  labelNameRules: {
    labelRequired: '请输入名称',
    labelLessThan100Chars: '名称必须少于100个字符',
    duplicated: '标签名已经被使用'
  },
  keyNameRules: {
    duplicated: '键已经被使用'
  },
  userNameRules: {
    userNameRequired: '请输入用户名',
    userNameLessThan30Chars: '用户名必须少于30个字符'
  },
  roleRules: {
    roleRequired: '请输入角色'
  },
  projectName: {
    required: '请输入项目名称',
    maxLength: '项目名称必须少于100个字符'
  },
  description: {
    required: '请输入描述'
  },
  fileFormatRules: {
    fileFormatRequired: '请输入文件类型'
  },
  uploadFileRules: {
    fileRequired: '请输入文件',
    fileLessThan1MB: '文件大小必须小于 100 MB!'
  },
  passwordRules: {
    passwordRequired: '请输入密码',
    passwordLessThan30Chars: '密码必须小于30个字符'
  }
}
