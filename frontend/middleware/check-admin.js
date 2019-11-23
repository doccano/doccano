export default function ({ store, route, redirect }) {
  const role = store.getters['projects/getCurrentUserRole']
  if (!role.is_project_admin) {
    redirect('/projects/' + route.params.id)
  }
}
