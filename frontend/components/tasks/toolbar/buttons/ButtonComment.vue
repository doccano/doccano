<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        icon
        v-on="on"
        @click="$emit('click:comment')"
      >
        <v-icon>
          mdi-chat
        </v-icon>
      </v-btn>
    </template>
    <span>{{ $t('annotation.commentTooltip') }}</span>
  </v-tooltip>
</template>
