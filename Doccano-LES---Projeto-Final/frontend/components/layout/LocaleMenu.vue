<template>
  <v-menu open-on-hover offset-y z-index="200">
    <template #activator="{ on }">
      <v-btn text v-on="on">
        {{ $i18n.locale }}
        <v-icon>{{ mdiMenuDown }}</v-icon>
      </v-btn>
    </template>
    <v-list v-for="locale in $i18n.locales" :key="locale.code">
      <nuxt-link
        class="v-list-item v-list-item--link"
        :class="$vuetify.theme.dark ? 'theme--dark' : 'theme--light'"
        :to="switchLocalePath(locale.code)"
      >
        {{ locale.name }}
      </nuxt-link>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMenuDown } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      mdiMenuDown
    }
  }
})
</script>
