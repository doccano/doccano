const validateItemPage = async ({ params, query, app }: { params: any; query: any; app: any }) => {
  if (!/^\d+$/.test(params.id)) {
    return false
  }
  if (!['category', 'span', 'relation'].includes(query.type as string)) {
    return false
  }
  const project = await app.$services.project.findById(params.id)
  return project.canDefineLabel
}

const validateEditPage = ({ params, query, app }: { params: any; query: any; app: any }) => {
  if (!validateItemPage({ params, query, app })) {
    return false
  }
  if (!/^\d+$/.test(params.label_id)) {
    return false
  }
  return true
}

export { validateItemPage, validateEditPage }
