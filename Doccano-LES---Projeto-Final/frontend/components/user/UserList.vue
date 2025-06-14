<template>
  <div>
    <!-- Alerta de erro de conexão -->
    <v-alert
      v-if="databaseError"
      type="error"
      dismissible
      class="mb-4"
    >
      A conexão com a base de dados falhou. Por favor, tente novamente mais tarde.
    </v-alert>

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
      <!-- Campo de busca -->
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

      <!-- Chip para Superuser -->
      <template #[`item.isSuperUser`]="props">
        <v-chip :color="props.item.isSuperUser ? 'blue' : 'grey'">
          {{ props.item.isSuperUser ? 'Sim' : 'Não' }}
        </v-chip>
      </template>

      <!-- Chip para Staff -->
      <template #[`item.isStaff`]="props">
        <v-chip :color="props.item.isStaff ? 'blue' : 'grey'">
          {{ props.item.isStaff ? 'Sim' : 'Não' }}
        </v-chip>
      </template>

      <!-- Ações (ícone de editar) -->
      <template #[`item.actions`]="{ item }">
        <v-icon small @click="$emit('editUser', item)">
          {{ mdiPencil }}
        </v-icon>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { mdiMagnify, mdiPencil } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { UserDTO } from '~/services/application/user/userData'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<UserDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<UserDTO[]>,
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
      mdiMagnify,
      databaseError: false,
      checkConnectionInterval: null as number | null
    }
  },

  computed: {
    headers() {
      const headers = [
        { text: this.$t('Username'), value: 'username', sortable: true },
        { text: this.$t('First Name'), value: 'first_name', sortable: true },
        { text: this.$t('Last Name'), value: 'last_name', sortable: true },
        { text: this.$t('Email'), value: 'email', sortable: true },
        { text: this.$t('Superuser'), value: 'isSuperUser', sortable: true },
        { text: this.$t('Staff'), value: 'isStaff', sortable: true }
      ]
      if (!this.disableEdit) {
        headers.push({ text: 'Actions', value: 'actions', sortable: false })
      }
      return headers
    }
  },

  mounted() {
    // Inicia a verificação da conexão a cada 2 segundos
    this.startConnectionCheck()
  },

  beforeDestroy() {
    // Limpa o intervalo quando o componente é destruído
    this.stopConnectionCheck()
  },

  methods: {
    async checkDatabaseConnection() {
      try {
        // Tenta buscar os usuários para verificar a conexão
        await this.$services.user.list()
        this.databaseError = false
      } catch (error) {
        console.error('Erro de conexão com o banco de dados:', error)
        this.databaseError = true
      }
    },

    startConnectionCheck() {
      // Faz a primeira verificação imediatamente
      this.checkDatabaseConnection()
      
      // Configura o intervalo para verificar a cada 2 segundos
      this.checkConnectionInterval = window.setInterval(() => {
        this.checkDatabaseConnection()
      }, 2000)
    },

    stopConnectionCheck() {
      if (this.checkConnectionInterval) {
        clearInterval(this.checkConnectionInterval)
        this.checkConnectionInterval = null
      }
    }
  }
})
</script>
