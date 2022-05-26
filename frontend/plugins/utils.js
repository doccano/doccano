export const idealColor = function (hexString) {
  // W3c offers a formula for calculating ideal color:
  // https://www.w3.org/TR/AERT/#color-contrast
  const r = parseInt(hexString.substr(1, 2), 16)
  const g = parseInt(hexString.substr(3, 2), 16)
  const b = parseInt(hexString.substr(5, 2), 16)
  return (r * 299 + g * 587 + b * 114) / 1000 < 128 ? '#ffffff' : '#000000'
}

export const translatedRoles = function (roles, mappings) {
  roles.forEach((role) => {
    role.translatedName = translateRole(role.name, mappings)
  })
  return roles
}

export const translateRole = function (role, mappings) {
  if (role === 'project_admin') {
    return mappings.projectAdmin
  } else if (role === 'annotator') {
    return mappings.annotator
  } else if (role === 'annotation_approver') {
    return mappings.annotationApprover
  } else {
    return mappings.undefined
  }
}
