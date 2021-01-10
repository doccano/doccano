export default async function({ app, store, route, redirect }) {
  if (store.getters['projects/isEmpty']) {
    await store.dispatch('projects/setCurrentProject', route.params.id)
  }
  const role = store.getters['projects/getCurrentUserRole']
  const projectRoot = app.localePath('/projects/' + route.params.id)
  const path = route.fullPath.replace(/\/$/g, '')
  if (!role.is_project_admin && path !== projectRoot) {
    return redirect(projectRoot)
  }
}
