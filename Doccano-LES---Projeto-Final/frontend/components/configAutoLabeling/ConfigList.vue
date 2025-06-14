<template>
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="items.toArray()"
    :loading="isLoading"
    :no-data-text="$t('vuetify.noDataAvailable')"
    item-key="id"
    :loading-text="$t('generic.loading')"
    show-select
  >
    <template #top>
      <div class="ma-4">
        <v-btn class="primary text-capitalize" @click="dialogCreate = true">
          {{ $t('generic.create') }}
        </v-btn>
        <v-btn
          class="text-capitalize ms-2"
          :disabled="!isDeletable()"
          outlined
          @click="dialogDelete = true"
        >
          {{ $t('generic.delete') }}
        </v-btn>
        <v-dialog v-model="dialogCreate">
          <config-creation-form
            @onCreate="
              onCreate()
              dialogCreate = false
            "
          />
        </v-dialog>
        <v-dialog v-model="dialogDelete">
          <confirm-form
            :items="selected"
            title="Delete Config"
            message="Are you sure you want to delete these configs?"
            item-key="modelName"
            @ok="
              remove()
              dialogDelete = false
            "
            @cancel="dialogDelete = false"
          />
        </v-dialog>
      </div>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import ConfigCreationForm from './ConfigCreationForm.vue'
import ConfirmForm from '@/components/utils/ConfirmForm.vue'
import { ConfigItemResponse } from '@/repositories/autoLabeling/config/apiConfigRepository'
import { ConfigItemList } from '~/domain/models/autoLabeling/config'

export default Vue.extend({
  components: {
    ConfirmForm,
    ConfigCreationForm
  },

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      isLoading: false as Boolean,
      items: ConfigItemList.valueOf([]) as ConfigItemList,
      selected: [] as ConfigItemResponse[],
      headers: [
        {
          text: 'Model name',
          align: 'left',
          value: 'modelName',
          sortable: false
        }
      ]
    }
  },

  async created(): Promise<void> {
    this.isLoading = true
    this.items = await this.$repositories.config.list(this.$route.params.id)
    this.isLoading = false
  },

  methods: {
    async remove(): Promise<void> {
      this.isLoading = true
      const projectId = this.$route.params.id
      for (const item of this.selected) {
        await this.$repositories.config.delete(projectId, item.id)
      }
      this.items = await this.$repositories.config.list(projectId)
      this.selected = []
      this.isLoading = false
    },
    isDeletable(): boolean {
      return this.selected.length > 0
    },
    async onCreate() {
      this.isLoading = true
      this.items = await this.$repositories.config.list(this.$route.params.id)
      this.isLoading = false
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
