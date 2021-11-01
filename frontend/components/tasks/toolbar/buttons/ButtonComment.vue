<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn
        icon
        v-on="on"
        @click="$emit('click:comment')"
      >
        <v-icon>
          mdi-message-text
        </v-icon>
      </v-btn>
    </template>
    <span>{{ $t('annotation.commentTooltip') }}</span>
  </v-tooltip>
</template>
