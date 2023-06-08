import { NuxtAppOptions } from '@nuxt/types'
import _ from 'lodash'

export default _.debounce(async ({ app, route, redirect }: NuxtAppOptions) => {
  const member = await app.$repositories.member.fetchMyRole(route.params.id)
  const projectRoot = app.localePath('/projects/' + route.params.id)
  const path = route.fullPath.replace(/\/$/g, '')

  if (!member.isProjectAdmin && path !== projectRoot) {
    return redirect(app.localePath('/projects/' + route.params.id))
  }
}, 1000)
