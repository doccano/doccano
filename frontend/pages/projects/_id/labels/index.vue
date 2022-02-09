<template>
  <v-card>
    <v-tabs v-if="hasMultiType" v-model="tab">
      <v-tab class="text-capitalize">Category</v-tab>
      <v-tab class="text-capitalize">Span</v-tab>
    </v-tabs>
    <v-card-title>
      <action-menu
        @create="$router.push('labels/add?type=' + labelType)"
        @upload="dialogUpload=true"
        @download="download"
      />
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete=true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogUpload">
        <form-upload
          :error-message="errorMessage"
          @cancel="closeUpload"
          @clear="clearErrorMessage"
          @upload="upload"
        />
      </v-dialog>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>
    <label-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      @edit="editItem"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ActionMenu from '@/components/label/ActionMenu.vue'
import FormDelete from '@/components/label/FormDelete.vue'
import FormUpload from '@/components/label/FormUpload.vue'
import LabelList from '@/components/label/LabelList.vue'
import { LabelDTO } from '~/services/application/label/labelData'
import { ProjectDTO } from '~/services/application/project/projectData'

export default Vue.extend({

  components: {
    ActionMenu,
    FormDelete,
    FormUpload,
    LabelList
  },
  layout: 'project',

  validate({ params, app }) {
    if (/^\d+$/.test(params.id)) {
      return app.$services.project.findById(params.id)
      .then((res:ProjectDTO) => {
        return res.canDefineLabel
      })
    }
    return false
  },

  data() {
    return {
      dialogDelete: false,
      dialogUpload: false,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      isLoading: false,
      errorMessage: '',
      tab: null,
      project: {} as ProjectDTO,
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    hasMultiType(): boolean {
      if ('projectType' in this.project) {
        return this.project.projectType === 'IntentDetectionAndSlotFilling'
      } else {
        return false
      }
    },

    labelType(): string {
      if (this.hasMultiType) {
        if (this.tab === 0) {
          return 'category'
        } else {
          return 'span'
        }
      } else if (this.project.projectType.endsWith('Classification')) {
        return 'category'
      } else {
        return 'span'
      }
    },

    service(): any {
      if (!('projectType' in this.project)) {
        return
      }
      if (this.hasMultiType) {
        if (this.tab === 0) {
          return this.$services.categoryType
        } else {
          return this.$services.spanType
        }
      } else if (this.project.projectType.endsWith('Classification')) {
        return this.$services.categoryType
      } else {
        return this.$services.spanType
      }
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

    async upload(file: File) {
      try {
        await this.service.upload(this.projectId, file)
        this.list()
        this.closeUpload()
      } catch(e) {
        this.errorMessage = e.message
      }
    },

    closeUpload() {
      this.clearErrorMessage()
      this.dialogUpload = false
    },

    clearErrorMessage() {
      this.errorMessage = ''
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
