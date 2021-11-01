<template>
  <v-menu
    open-on-hover
    offset-y
  >
    <template #activator="{ on }">
      <v-btn
        text
        v-on="on"
      >
        {{ $i18n.locale }}
        <v-icon>mdi-menu-down</v-icon>
      </v-btn>
    </template>
    <v-list
      v-for="locale in $i18n.locales"
      :key="locale.code"
    >
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
