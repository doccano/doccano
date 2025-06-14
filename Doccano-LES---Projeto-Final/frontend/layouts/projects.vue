<template>
  <v-app>
    <the-header />
    <v-main>
      <v-container fluid fill-height>
        <v-layout justify-center>
          <v-flex>
            <nuxt />
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TheHeader from '~/components/layout/TheHeader'

export default {
  components: {
    TheHeader
  }
}
</script>
