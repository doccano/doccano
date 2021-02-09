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
    <template v-slot:top>
      <confirm-dialog
        :disabled="!isDeletable()"
        :items="selected"
        :title="$t('overview.deleteProjectTitle')"
        :message="$t('overview.deleteProjectMessage')"
        :button-true-text="$t('generic.yes')"
        :button-false-text="$t('generic.cancel')"
        item-key="modelName"
        @ok="remove"
      />
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import { headers, ConfigItemList } from '@/models/config/config-item-list'
import { ConfigApplicationService } from '@/services/application/config.service'
import { FromApiConfigItemListRepository } from '@/repositories/config/api'
import ConfirmDialog from '@/components/organisms/utils/ConfirmDialog'

export default Vue.extend({
  components: {
    ConfirmDialog
  },

  data() {
    return {
      isLoading: false,
      items: ConfigItemList.valueOf([]),
      selected: [],
      headers
    }
  },

  computed: {
    configService(): ConfigApplicationService {
      const configRepository = new FromApiConfigItemListRepository()
      const configService = new ConfigApplicationService(configRepository)
      return configService
    }
  },

  async created(): Promise<void> {
    this.isLoading = true
    this.items = await this.configService.list(this.$route.params.id)
    this.isLoading = false
  },

  methods: {
    async remove(): Promise<void> {
      this.isLoading = true
      const projectId = this.$route.params.id
      for (const item of this.selected) {
        await this.configService.delete(projectId, item.id)
      }
      this.items = await this.configService.list(projectId)
      this.isLoading = false
    },
    isDeletable(): boolean {
      return this.selected.length > 0
    }
  }
})
</script>
