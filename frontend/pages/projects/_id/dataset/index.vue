<template>
  <v-card>
    <v-card-title v-if="isProjectAdmin">
      <action-menu
        @upload="$router.push('dataset/import')"
        @download="$router.push('dataset/export')"
        @assign="dialogAssignment = true"
        @reset="dialogReset = true"
      />
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-spacer />
      <v-btn
        :disabled="!item.count"
        class="text-capitalize"
        color="error"
        @click="dialogDeleteAll = true"
      >
        {{ $t('generic.deleteAll') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          :item-key="itemKey"
          @cancel="dialogDelete = false"
          @remove="remove"
        />
      </v-dialog>
      <v-dialog v-model="dialogDeleteAll">
        <form-delete-bulk @cancel="dialogDeleteAll = false" @remove="removeAll" />
      </v-dialog>
      <v-dialog v-model="dialogAssignment">
        <form-assignment @assigned="assigned" @cancel="dialogAssignment = false" />
      </v-dialog>
      <v-dialog v-model="dialogReset">
        <form-reset-assignment @cancel="dialogReset = false" @reset="resetAssignment" />
      </v-dialog>
    </v-card-title>
    <image-list
      v-if="project.isImageProject"
      v-model="selected"
      :items="item.items"
      :is-admin="user.isProjectAdmin"
      :is-loading="isLoading"
      :members="members"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
      @assign="assign"
      @unassign="unassign"
    />
    <audio-list
      v-else-if="project.isAudioProject"
      v-model="selected"
      :items="item.items"
      :is-admin="user.isProjectAdmin"
      :is-loading="isLoading"
      :members="members"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
      @assign="assign"
      @unassign="unassign"
    />
    <document-list
      v-else
      v-model="selected"
      :items="item.items"
      :is-admin="user.isProjectAdmin"
      :is-loading="isLoading"
      :members="members"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
      @edit="editItem"
      @assign="assign"
      @unassign="unassign"
    />
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import { mapGetters } from 'vuex'
import Vue from 'vue'
import { NuxtAppOptions } from '@nuxt/types'
import DocumentList from '@/components/example/DocumentList.vue'
import FormAssignment from '~/components/example/FormAssignment.vue'
import FormDelete from '@/components/example/FormDelete.vue'
import FormDeleteBulk from '@/components/example/FormDeleteBulk.vue'
import FormResetAssignment from '~/components/example/FormResetAssignment.vue'
import ActionMenu from '~/components/example/ActionMenu.vue'
import AudioList from '~/components/example/AudioList.vue'
import ImageList from '~/components/example/ImageList.vue'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'
import { ExampleDTO, ExampleListDTO } from '~/services/application/example/exampleData'
import { MemberItem } from '~/domain/models/member/member'

export default Vue.extend({
  components: {
    ActionMenu,
    AudioList,
    DocumentList,
    ImageList,
    FormAssignment,
    FormDelete,
    FormDeleteBulk,
    FormResetAssignment
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, query }: NuxtAppOptions) {
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  },

  data() {
    return {
      dialogDelete: false,
      dialogDeleteAll: false,
      dialogAssignment: false,
      dialogReset: false,
      item: {} as ExampleListDTO,
      selected: [] as ExampleDTO[],
      members: [] as MemberItem[],
      user: {} as MemberItem,
      isLoading: false,
      isProjectAdmin: false
    }
  },

  async fetch() {
    this.isLoading = true
    this.item = await this.$services.example.list(this.projectId, this.$route.query)
    this.user = await this.$repositories.member.fetchMyRole(this.projectId)
    if (this.user.isProjectAdmin) {
      this.members = await this.$repositories.member.list(this.projectId)
    }
    this.isLoading = false
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    itemKey(): string {
      if (this.project.isImageProject || this.project.isAudioProject) {
        return 'filename'
      } else {
        return 'text'
      }
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  async created() {
    const member = await this.$repositories.member.fetchMyRole(this.projectId)
    this.isProjectAdmin = member.isProjectAdmin
  },

  methods: {
    async remove() {
      await this.$services.example.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    async removeAll() {
      await this.$services.example.bulkDelete(this.projectId, [])
      this.$fetch()
      this.dialogDeleteAll = false
      this.selected = []
    },

    updateQuery(query: object) {
      this.$router.push(query)
    },

    movePage(query: object) {
      const link = getLinkToAnnotationPage(this.projectId, this.project.projectType)
      this.updateQuery({
        path: this.localePath(link),
        query
      })
    },

    editItem(item: ExampleDTO) {
      this.$router.push(`dataset/${item.id}/edit`)
    },

    async assign(exampleId: number, userId: number) {
      await this.$repositories.assignment.assign(this.projectId, exampleId, userId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async unassign(assignmentId: string) {
      await this.$repositories.assignment.unassign(this.projectId, assignmentId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async assigned() {
      this.dialogAssignment = false
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async resetAssignment() {
      this.dialogReset = false
      await this.$repositories.assignment.reset(this.projectId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
