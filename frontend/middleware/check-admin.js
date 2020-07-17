export default function({ store, route, redirect }) {
  const role = store.getters['projects/getCurrentUserRole']
  const projectRoot = '/projects/' + route.params.id
  const path = route.fullPath.replace(/\/$/g, '')
  if (!role.is_project_admin && path !== projectRoot) {
    return redirect(projectRoot)
  }
}
