export default async function({ store }) {
  if (!store.getters['auth/isAuthenticated']) {
    await store.dispatch('auth/initAuth')
  }
}
