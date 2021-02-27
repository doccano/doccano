<template>
  <v-card>
    <v-card-title>
      <action-menu
        @create="dialogCreate=true"
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
      <v-dialog v-model="dialogCreate">
        <form-create
          v-model="editedItem"
          :used-keys="usedKeys"
          :used-names="usedNames"
          @cancel="close"
          @save="save"
        />
      </v-dialog>
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
import { LabelDTO } from '@/services/application/label.service'
import ActionMenu from '@/components/label/ActionMenu.vue'
import FormCreate from '@/components/label/FormCreate.vue'
import FormDelete from '@/components/label/FormDelete.vue'
import FormUpload from '@/components/label/FormUpload.vue'
import LabelList from '@/components/label/LabelList.vue'

export default Vue.extend({
  layout: 'project',

  components: {
    ActionMenu,
    FormCreate,
    FormDelete,
    FormUpload,
    LabelList
  },

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      dialogUpload: false,
      editedIndex: -1,
      editedItem: {
        text: '',
        prefix_key: null,
        suffix_key: null,
        background_color: '#2196F3',
        text_color: '#ffffff'
      } as LabelDTO,
      defaultItem: {
        text: '',
        prefix_key: null,
        suffix_key: null,
        background_color: '#2196F3',
        text_color: '#ffffff'
      } as LabelDTO,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      isLoading: false,
      errorMessage: ''
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
    },
    usedNames(): string[] {
      return this.items.map(item => item.text)
    },
    usedKeys(): string[] {
      return this.items.map(item => item.suffix_key).filter(item => item !==null) as string[]
    }
  },

  created() {
    this.list()
  },

  methods: {
    async list() {
      this.isLoading = true
      this.items = await this.$services.label.list(this.projectId)
      this.isLoading = false
    },

    async create(item: LabelDTO) {
      await this.$services.label.create(this.projectId, item)
    },

    async update(item: LabelDTO) {
      await this.$services.label.update(this.projectId, item)
    },

    save() {
      if (this.editedIndex > -1) {
        this.update(this.editedItem)
      } else {
        this.create(this.editedItem)
      }
      this.list()
      this.close()
    },

    close() {
      this.dialogCreate = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    async remove() {
      await this.$services.label.bulkDelete(this.projectId, this.selected)
      this.list()
      this.dialogDelete = false
      this.selected = []
    },

    async download() {
      await this.$services.label.export(this.projectId)
    },

    async upload(file: File) {
      try {
        await this.$services.label.upload(this.projectId, file)
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
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogCreate = true
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
