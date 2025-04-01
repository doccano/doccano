<template>
  <v-card>
    <v-card-title class="button-container">
      <v-btn color="primary" class="text-lowercase" @click="$router.push('perspectives/add')">
        Create
      </v-btn>
      <v-btn 
        :disabled="selected.length === 0" 
        :class="{ 'active-delete': selected.length > 0, 'text-lowercase': true }" 
        @click="deletePerspective">
        Delete
      </v-btn>
    </v-card-title>
    <perspective-list v-model="selected" :items="items" :is-loading="isLoading" />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import PerspectiveList from '@/components/perspective/PerspectiveList.vue'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData'

export default Vue.extend({
  components: {
    PerspectiveList
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'isSuperUser', 'setCurrentProject'],

  data() {
    return {
      items: [] as PerspectiveDTO[],
      selected: [] as PerspectiveDTO[],
      isLoading: false,
      tab: 0,
      drawerLeft: null
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff', 'isSuperUser'])
  },

  mounted() {
    this.fetchPerspectives()
  },

  methods: {
    async fetchPerspectives() {
      this.isLoading = true
      try {
        // Obtém o projectId a partir dos parâmetros da rota
        const projectId = this.$route.params.id
        const response = await this.$services.perspective.list(projectId)
        this.items = response
      } catch (error) {
        console.error('Erro ao buscar perspectivas:', error)
      } finally {
        this.isLoading = false
      }
    },

    deletePerspective() {
      if (this.selected.length === 0) return;
      if (confirm('Tem certeza que deseja excluir esta perspectiva?')) {
        console.log('Perspectiva deletada')
        // Adicionar lógica de deleção aqui
      }
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}

.button-container {
  display: flex;
  gap: 16px;
}

.v-btn:disabled {
  color: #b0b0b0 !important;
  border: 1px solid #b0b0b0 !important;
  background-color: transparent !important;
}

.active-delete {
  color: black !important;
  border: 1px solid black !important;
  background-color: transparent !important;
}

.text-lowercase {
  text-transform: none !important;
}
</style>
