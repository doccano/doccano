export default async function ({ store, route }) {
  const project = store.getters['projects/currentProject']
  const isEmpty = Object.keys(project).length === 0 && project.constructor === Object
  if (isEmpty) {
    await store.dispatch('projects/setCurrentProject', route.params.id)
  }
}
