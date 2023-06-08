import { NuxtAppOptions } from '@nuxt/types'

export default async ({ app, route, redirect }: NuxtAppOptions) => {
  const project = app.store.getters['projects/currentProject']
  const isNotSet = Object.keys(project).length === 0 && project.constructor === Object
  if (isNotSet || project.id !== route.params.id) {
    try {
      await app.store.dispatch('projects/setCurrentProject', route.params.id)
    } catch (e) {
      redirect('/projects')
    }
  }
}
