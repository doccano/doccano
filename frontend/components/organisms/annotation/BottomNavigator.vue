<template>
  <v-bottom-navigation
    absolute
    hide-on-scroll
    background-color="transparent"
    class="elevation-0"
  >
    <v-btn>
      <span>Prev</span>
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>

    <v-btn value="done">
      <span>Done</span>
      <v-icon>mdi-check</v-icon>
    </v-btn>

    <v-btn value="guide">
      <span>Guideline</span>
      <v-icon>mdi-book-open-outline</v-icon>
    </v-btn>

    <v-btn>
      <span>Next</span>
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>
