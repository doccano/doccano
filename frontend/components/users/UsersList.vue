<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :options.sync="options"
      :server-items-length="total"
      :search="search"
      :loading="isLoading"
      item-key="id"
      show-select
      class="elevation-1"
      @input="$emit('input', $event)"
      @update:options="updateQuery({ query: $route.query })"
    >
      <!-- Campo de Pesquisa -->
      <template #top>
        <v-text-field
          v-model="search"
          :prepend-inner-icon="mdiMagnify"
          label="Pesquisar"
          single-line
          hide-details
          filled
          @input="emitSearch"
        />
      </template>

      <!-- Nome de Usuário com ícone -->
      <template #[`item.username`]="{ item }">
        <v-btn icon small @click="showDetails(item)" title="Ver detalhes">
          <v-icon>{{ mdiChevronDown }}</v-icon>
        </v-btn>
        {{ item.username }}
      </template>

      <!-- Coluna Staff (true/false) -->
      <template #[`item.isStaff`]="{ item }">
        {{ item.isStaff }}
      </template>

      <!-- Coluna Superuser (true/false) -->
      <template #[`item.isSuperuser`]="{ item }">
        {{ item.isSuperuser }}
      </template>

      <!-- Coluna Ações -->
      <template #[`item.actions`]="{ item }">
        <v-icon small @click="showDetails(item)" color="primary" class="cursor-pointer" title="Ver detalhes">
          mdi-eye
        </v-icon>
      </template>
    </v-data-table>

    <!-- Diálogo de Detalhes -->
    <v-dialog v-model="showDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6">
          <v-icon left color="deep-purple accent-4">mdi-account-circle</v-icon>
          User Details
        </v-card-title>
        <v-card-text v-if="selectedUser">
             <p><strong>ID:</strong> {{ selectedUser.id }}</p>
            <p><strong>💗 Username:</strong> {{ selectedUser.username }}</p>
            <p><strong>🧍 Primeiro Nome:</strong> {{ selectedUser.firstName }}</p>
            <p><strong>🧍 Último Nome:</strong> {{ selectedUser.lastName }}</p>
            <p><strong>📧 Email:</strong> {{ selectedUser.email || 'Não informado' }}</p>
            <p><strong>👥 Staff:</strong> {{ selectedUser.isStaff ? '✅ Sim' : '❌ Não' }}</p>
            <p><strong>🛡️ Superuser:</strong> {{ selectedUser.isSuperuser ? '✅ Sim' : '❌ Não' }}</p>
                </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="showDialog = false">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { mdiMagnify, mdiChevronDown } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { UserItem } from '~/domain/models/user'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      required: true
    },
    items: {
      type: Array as PropType<UserItem[]>,
      required: true
    },
    value: {
      type: Array as PropType<UserItem[]>,
      required: true
    },
    total: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      search: this.$route.query.q || '',
      options: {} as DataOptions,
      mdiMagnify,
      mdiChevronDown,
      showDialog: false,
      selectedUser: null as UserItem | null
    }
  },
  computed: {
    headers() {
  return [
    { text: 'Username', value: 'username', sortable: true },
      { text: 'First_name', value: 'firstName' },
      { text: 'Last_name', value: 'lastName' },
    { text: 'Staff', value: 'isStaff' },
    { text: 'Superuser', value: 'isSuperuser' },
    { text: 'Active', value: 'isActive' },
  ]
}

  },
  watch: {
    search() {
      this.emitSearch()
    }
  },
  methods: {
    emitSearch() {
      this.$emit('search', this.search)
    },
    updateQuery(payload: any) {
  const { sortBy, sortDesc } = this.options

  const query = {
    ...payload.query,
    sortBy: sortBy?.[0] || '',
    sortDesc: sortDesc?.[0] || false,
    q: this.search
  }

  this.$emit('update:query', { query })
}
,
    showDetails(user: UserItem) {
      this.selectedUser = user
      this.showDialog = true
    }
  }
})
</script>
