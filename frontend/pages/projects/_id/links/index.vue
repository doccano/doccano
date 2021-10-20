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
import { LinkTypeDTO } from '~/services/application/links/linkData'
import { ProjectDTO } from '~/services/application/project/projectData'

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
    this.items = await this.$services.linkTypes.list(this.projectId)
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
        color: '#ffffff'
      } as LinkTypeDTO,
      defaultItem: {
        text: '',
        color: '#ffffff'
      } as LinkTypeDTO,
      items: [] as LinkTypeDTO[],
      selected: [] as LinkTypeDTO[],
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
    }
  },

  methods: {
    async create() {
      await this.$services.linkTypes.create(this.projectId, this.editedItem)
    },

    async update() {
      await this.$services.linkTypes.update(this.projectId, this.editedItem)
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
      await this.$services.linkTypes.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    clearErrorMessage() {
      this.errorMessage = ''
    },

    editItem(item: LinkTypeDTO) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogCreate = true
    }
  },

  validate({ params, app }) {
    if (/^\d+$/.test(params.id)) {
      return app.$services.project.findById(params.id)
      .then((res:ProjectDTO) => {
        return res.canDefineRelation
      })
    }
    return false
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
