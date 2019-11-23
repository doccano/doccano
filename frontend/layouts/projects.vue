<template>
  <v-app>
    <the-header />
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
  </v-app>
</template>

<script>
import TheHeader from '~/components/organisms/layout/TheHeader'

export default {
  components: {
    TheHeader
  }
}
</script>
