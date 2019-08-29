<template>
  <base-layout>
    <template #content>
      <v-content>
        <v-container
          fluid
          fill-height
        >
          <v-layout
            justify-center
          >
            <v-flex>
              <nuxt />
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
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
