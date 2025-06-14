import { NuxtAppOptions } from '@nuxt/types'
import _ from 'lodash'

export default _.debounce(async ({ app, route, redirect }: NuxtAppOptions) => {
  const project = app.store.getters['projects/currentProject']
  if (project.id !== route.params.id) {
    try {
      await app.store.dispatch('projects/setCurrentProject', route.params.id)
    } catch (e) {
      redirect('/projects')
    }
  }
}, 1000)
