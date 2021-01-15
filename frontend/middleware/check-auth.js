export default function (context) {
  context.store.dispatch('auth/initAuth', context.req)
}
