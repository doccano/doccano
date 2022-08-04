<template>
  <v-card>
    <v-tabs v-if="labelTypes.length > 1" v-model="tab">
      <v-tab v-for="label in labelTypes" :key="label" class="text-capitalize">{{ label }}</v-tab>
    </v-tabs>
    <v-card-title>
      <action-menu
        @create="$router.push('labels/add?type=' + labelType)"
        @upload="$router.push('labels/import?type=' + labelType)"
        @download="download"
      />
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>
    <label-list v-model="selected" :items="items" :is-loading="isLoading" @edit="editItem" />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ActionMenu from '@/components/label/ActionMenu.vue'
import FormDelete from '@/components/label/FormDelete.vue'
import LabelList from '@/components/label/LabelList.vue'
import { LabelDTO } from '~/services/application/label/labelData'
import { ProjectDTO } from '~/services/application/project/projectData'

export default Vue.extend({
  components: {
    ActionMenu,
    FormDelete,
    LabelList
  },

  layout: 'project',

  async validate({ params, app }) {
    if (!/^\d+$/.test(params.id)) {
      return false
    }
    const project = await app.$services.project.findById(params.id)
    return project.canDefineLabel
  },

  data() {
    return {
      dialogDelete: false,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      isLoading: false,
      tab: 0,
      project: {} as ProjectDTO
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    labelTypes(): string[] {
      const types: string[] = []
      if (this.project.canDefineCategory) {
        types.push('category')
      }
      if (this.project.canDefineSpan) {
        types.push('span')
      }
      if (this.project.canDefineRelation) {
        types.push('relation')
      }
      return types
    },

    labelType(): string {
      return this.labelTypes[this.tab]
    },

    service(): any {
      if (!('projectType' in this.project)) {
        return
      }
      const services = []
      if (this.project.canDefineCategory) {
        services.push(this.$services.categoryType)
      }
      if (this.project.canDefineSpan) {
        services.push(this.$services.spanType)
      }
      if (this.project.canDefineRelation) {
        services.push(this.$services.relationType)
      }
      return services[this.tab]
    }
  },

  watch: {
    tab() {
      this.list()
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    await this.list()
  },

  methods: {
    async list() {
      this.isLoading = true
      this.items = await this.service.list(this.projectId)
      this.isLoading = false
    },

    async remove() {
      await this.service.bulkDelete(this.projectId, this.selected)
      this.list()
      this.dialogDelete = false
      this.selected = []
    },

    async download() {
      await this.service.export(this.projectId)
    },

    editItem(item: LabelDTO) {
      this.$router.push(`labels/${item.id}/edit?type=${this.labelType}`)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
