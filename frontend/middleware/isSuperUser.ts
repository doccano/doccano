import { Context } from '@nuxt/types'

export default function ({ app, store, redirect }: Context) {
  const isSuperUser = store.getters['auth/isSuperUser']

  if (!isSuperUser) {
    return redirect(app.localePath('/projects'))
  }
}
