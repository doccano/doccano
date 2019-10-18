<template>
  <v-bottom-navigation
    absolute
    hide-on-scroll
    background-color="transparent"
    class="elevation-0"
  >
    <v-tooltip top>
      <template v-slot:activator="{ on }">
        <v-btn v-on="on">
          <span>Prev</span>
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </template>
      <span>ctrl + ←</span>
    </v-tooltip>

    <v-btn value="done">
      <span>Done</span>
      <v-icon>mdi-check</v-icon>
    </v-btn>

    <v-btn value="guide">
      <span>Guideline</span>
      <v-icon>mdi-format-color-text</v-icon>
    </v-btn>

    <v-tooltip top>
      <template v-slot:activator="{ on }">
        <v-btn v-on="on">
          <span>Next</span>
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </template>
      <span>ctrl + →</span>
    </v-tooltip>
  </v-bottom-navigation>
</template>
