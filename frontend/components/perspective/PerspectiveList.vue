<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template #top>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template #[`item.questionsCount`]="{ item }">
      <span>{{ item.questions ? item.questions.length : 0 }}</span>
    </template>
    <template #[`item.membersCount`]="{ item }">
      <span>{{ item.members ? item.members.length : 0 }}</span>
    </template>
    <template #[`item.actions`]="{ item }">
      <v-icon small @click="$emit('edit', item)">
        {{ mdiPencil }}
      </v-icon>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMagnify, mdiPencil } from '@mdi/js'
import type { PropType } from 'vue'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData' // Ajuste o caminho conforme necessário

export default Vue.extend({
  name: 'PerspectiveList',
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<PerspectiveDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<PerspectiveDTO[]>,
      default: () => [],
      required: true
    },
    disableEdit: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      search: '',
      mdiPencil,
      mdiMagnify
    }
  },

  computed: {
    headers() {
      const headers = [
        { text: this.$t('ID'), value: 'id', sortable: true },
        { text: this.$t('Project'), value: 'project_id', sortable: true },
        { text: this.$t('Questions'), value: 'questionsCount', sortable: false },
        { text: this.$t('Members'), value: 'membersCount', sortable: false }
      ]
      if (!this.disableEdit) {
        headers.push({ text: this.$t('Actions'), value: 'actions', sortable: false })
      }
      return headers
    }
  }
})
</script>

<style scoped>
/* Adicione aqui os estilos necessários */
</style>
