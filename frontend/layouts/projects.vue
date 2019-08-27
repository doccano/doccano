<template>
  <base-layout>
    <template #content>
      <nuxt />
    </template>
  </base-layout>
</template>

<script>
import BaseLayout from '~/layouts/BaseLayout'

export default {
  components: {
    BaseLayout
  }
}
</script>
