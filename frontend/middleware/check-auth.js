export default async function(context) {
  await context.store.dispatch('auth/initAuth', context.req)
}
