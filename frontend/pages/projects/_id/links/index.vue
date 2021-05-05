<template>
  <v-card>
    <v-card-title>
      <action-menu
        @create="dialogCreate=true"
        @upload="dialogUpload=true"
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
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>

    <p>WORK IN PROGRESS... THIS WILL BECOME THE RELATIONS TYPE CRUD PAGE</p>

    <links-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      @edit="editItem"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ActionMenu from '@/components/links/ActionMenu.vue'
import FormCreate from '@/components/links/FormCreate.vue'
import FormDelete from '@/components/links/FormDelete.vue'
import LinksList from '~/components/links/LinksList.vue'
import { LinkDTO } from '~/services/application/links/linkData'

export default Vue.extend({
  layout: 'project',

  components: {
    ActionMenu,
    FormCreate,
    FormDelete,
    LinksList
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.links.list(this.projectId)
    this.isLoading = false
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
      } as LinkDTO,
      defaultItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#2196F3',
        textColor: '#ffffff'
      } as LinkDTO,
      items: [] as LinkDTO[],
      selected: [] as LinkDTO[],
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
      await this.$services.links.create(this.projectId, this.editedItem)
    },

    async update() {
      await this.$services.links.update(this.projectId, this.editedItem)
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
      await this.$services.links.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    clearErrorMessage() {
      this.errorMessage = ''
    },

    editItem(item: LinkDTO) {
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
