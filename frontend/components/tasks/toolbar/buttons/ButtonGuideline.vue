<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn
        icon
        v-on="on"
        @click="$emit('click:guideline')"
      >
        <v-icon>
          mdi-book-open-outline
        </v-icon>
      </v-btn>
    </template>
    <span>{{ $t('annotation.guidelineTooltip') }}</span>
  </v-tooltip>
</template>
