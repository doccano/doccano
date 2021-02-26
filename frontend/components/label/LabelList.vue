<template>
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, $t('generic.all')],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
  >
    <template v-slot:top>
      <v-toolbar flat>
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
            @cancel="close"
            @save="save"
          />
        </v-dialog>
        <v-dialog v-model="dialogUpload">
          <form-upload
            @cancel="dialogUpload=false"
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
      </v-toolbar>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template v-slot:[`item.background_color`]="props">
      <v-chip
        :color="props.item.background_color"
        :text-color="textColor(props.item.background_color)"
      >
        {{ props.item.background_color }}
      </v-chip>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon
        small
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import { LabelDTO } from '@/services/application/label.service'
import ActionMenu from './ActionMenu.vue'
import FormCreate from './FormCreate.vue'
import FormDelete from './FormDelete.vue'
import FormUpload from './FormUpload.vue'
import { idealColor } from '~/plugins/utils'

export default Vue.extend({
  components: {
    ActionMenu,
    FormCreate,
    FormDelete,
    FormUpload
  },

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      dialogUpload: false,
      headers: [
        { text: this.$t('generic.name'),    value: 'text' },
        { text: this.$t('labels.shortkey'), value: 'suffix_key' },
        { text: this.$t('labels.color'),    value: 'background_color' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
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
      isLoading: false,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      search: ''
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
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
      this.list()
      this.dialogCreate = false
    },

    async update(item: LabelDTO) {
      await this.$services.label.update(this.projectId, item)
      this.list()
      this.dialogCreate = false
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
      await this.$services.label.upload(this.projectId, file)
      this.list()
      this.dialogUpload = false
    },

    editItem(item: LabelDTO) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogCreate = true
    },

    close() {
      this.dialogCreate = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      if (this.editedIndex > -1) {
        this.update(this.editedItem)
      } else {
        this.create(this.editedItem)
      }
      this.close()
    },

    textColor(backgroundColor: string) {
      return idealColor(backgroundColor)
    }
  }  
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>