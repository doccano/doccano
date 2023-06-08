import { NuxtAppOptions } from '@nuxt/types'
import _ from 'lodash'

export default _.debounce(async ({ app, route, redirect }: NuxtAppOptions) => {
  const member = await app.$repositories.member.fetchMyRole(route.params.id)

  if (!member.isProjectAdmin) {
    return redirect(app.localePath('/projects/' + route.params.id))
  }
}, 1000)
