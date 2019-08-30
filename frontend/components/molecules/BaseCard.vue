<template>
  <v-card>
    <v-card-title class="grey lighten-2">
      {{ title }}
    </v-card-title>
    <v-container grid-list-sm>
      <v-layout wrap>
        <v-flex xs12>
          <slot name="content" />
        </v-flex>
      </v-layout>
    </v-container>
    <v-card-actions>
      <v-spacer />
      <slot name="actions" />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: '',
      required: true
    }
  }
}
</script>
