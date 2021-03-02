<template>
  <v-card>
    <v-card-title>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete=true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>
    <project-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ProjectList from '@/components/project/ProjectList.vue'
import { ProjectDTO } from '@/services/application/project.service'
import FormDelete from '~/components/project/FormDelete.vue'

export default Vue.extend({
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  components: {
    FormDelete,
    ProjectList,
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.project.list()
    this.isLoading = false
  },

  data() {
    return {
      dialogDelete: false,
      items: [] as ProjectDTO[],
      selected: [] as ProjectDTO[],
      isLoading: false
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
  },

  methods: {
    async remove() {
      await this.$services.project.bulkDelete(this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
