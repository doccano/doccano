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
      <div class="ma-4">
        <base-modal>
          <template v-slot:opener="modal">
            <v-btn
              class="primary text-capitalize"
              @click="modal.open"
            >
              {{ $t('generic.create') }}
            </v-btn>
          </template>
          <template v-slot:content="modal">
            <config-creation-form
              @onCreate="onCreate();modal.close()"
            />
          </template>
        </base-modal>
        <base-modal>
          <template v-slot:opener="modal">
            <v-btn
              :disabled="!isDeletable()"
              class="text-capitalize ms-2"
              outlined
              @click="modal.open"
            >
              {{ $t('generic.delete') }}
            </v-btn>
          </template>
          <template v-slot:content="modal">
            <confirm-form
              :items="selected"
              title="Delete Config"
              message="Are you sure you want to delete these configs?"
              item-key="modelName"
              @ok="remove();modal.close()"
              @cancel="modal.close"
            />
          </template>
        </base-modal>
      </div>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import { ConfigItemList } from '@/models/config/config-item-list'
import { ConfigApplicationService } from '@/services/application/config.service'
import { FromApiConfigItemListRepository, ConfigItemResponse } from '@/repositories/config/api'
import ConfirmForm from '@/components/organisms/utils/ConfirmForm.vue'
import BaseModal from '@/components/atoms/BaseModal.vue'
import ConfigCreationForm from '@/components/containers/settings/ConfigCreationForm.vue'

export default Vue.extend({
  components: {
    ConfirmForm,
    ConfigCreationForm,
    BaseModal
  },

  data() {
    return {
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
      this.selected = []
      this.isLoading = false
    },
    isDeletable(): boolean {
      return this.selected.length > 0
    },
    async onCreate() {
      this.isLoading = true
      this.items = await this.configService.list(this.$route.params.id)
      this.isLoading = false
    }
  }
})
</script>
