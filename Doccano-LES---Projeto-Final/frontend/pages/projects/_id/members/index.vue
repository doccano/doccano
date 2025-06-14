<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize" color="primary" @click.stop="dialogCreate = true">
        {{ $t('generic.add') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogCreate">
        <form-create
          v-model="editedItem"
          :error-message="errorMessage"
          @cancel="close"
          @save="save"
        />
      </v-dialog>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>
    <member-list v-model="selected" :items="items" :is-loading="isLoading" @edit="editItem" />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import FormDelete from '@/components/member/FormDelete.vue'
import MemberList from '@/components/member/MemberList.vue'
import FormCreate from '~/components/member/FormCreate.vue'
import { MemberItem } from '~/domain/models/member/member'

export default Vue.extend({
  components: {
    MemberList,
    FormCreate,
    FormDelete
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      editedIndex: -1,
      editedItem: {
        user: -1,
        role: -1,
        username: '',
        rolename: 'annotator'
      } as MemberItem,
      defaultItem: {
        user: -1,
        role: -1,
        username: '',
        rolename: 'annotator'
      } as MemberItem,
      items: [] as MemberItem[],
      selected: [] as MemberItem[],
      isLoading: false,
      errorMessage: ''
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      this.items = await this.$repositories.member.list(this.projectId)
    } catch (e) {
      this.$router.push(`/projects/${this.projectId}`)
    } finally {
      this.isLoading = false
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

  methods: {
    async create() {
      try {
        await this.$repositories.member.create(this.projectId, this.editedItem)
        this.close()
        this.$fetch()
      } catch (e: any) {
        this.errorMessage = e.response.data.detail
      }
    },

    async update() {
      try {
        await this.$repositories.member.update(this.projectId, this.editedItem)
        this.close()
        this.$fetch()
      } catch (e: any) {
        this.errorMessage = e.response.data.detail
      }
    },

    save() {
      if (this.editedIndex > -1) {
        this.update()
      } else {
        this.create()
      }
    },

    close() {
      this.dialogCreate = false
      this.errorMessage = ''
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    async remove() {
      await this.$repositories.member.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    editItem(item: MemberItem) {
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
