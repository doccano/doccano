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
          v-bind.sync="editedItem"
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
import ActionMenu from '@/components/label/ActionMenu.vue'
import FormCreate from '@/components/label/FormCreate.vue'
import FormDelete from '@/components/label/FormDelete.vue'
import FormUpload from '@/components/label/FormUpload.vue'
import LabelList from '@/components/label/LabelList.vue'
import { LabelDTO } from '~/services/application/label/labelData'
import { ProjectDTO } from '~/services/application/project/projectData'

export default Vue.extend({

  components: {
    ActionMenu,
    FormCreate,
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
      dialogCreate: false,
      dialogDelete: false,
      dialogUpload: false,
      editedIndex: -1,
      editedItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#2196F3',
        textColor: '#ffffff'
      } as LabelDTO,
      defaultItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#2196F3',
        textColor: '#ffffff'
      } as LabelDTO,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      isLoading: false,
      errorMessage: ''
    }
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.label.list(this.projectId)
    this.isLoading = false
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
    },
    usedNames(): string[] {
      const item = this.items[this.editedIndex] // to remove myself
      return this.items.filter(_ => _ !== item).map(item => item.text)
    },
    usedKeys(): string[] {
      const item = this.items[this.editedIndex] // to remove myself
      return this.items.filter(_ => _ !== item).map(item => item.suffixKey)
                       .filter(item => item !==null) as string[]
    }
  },

  methods: {
    async create() {
      await this.$services.label.create(this.projectId, this.editedItem)
    },

    async update() {
      await this.$services.label.update(this.projectId, this.editedItem)
    },

    save() {
      if (this.editedIndex > -1) {
        this.update()
      } else {
        this.create()
      }
      this.$fetch()
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
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    async download() {
      await this.$services.label.export(this.projectId)
    },

    async upload(file: File) {
      try {
        await this.$services.label.upload(this.projectId, file)
        this.$fetch()
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
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
