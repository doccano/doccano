<template>
  <v-card>
    <v-card-title>
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
    <comment-list
      v-model="selected"
      :items="item.items"
      :is-loading="isLoading"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
    />
  </v-card>
</template>

<script lang="ts">
import CommentList from '@/components/comment/CommentList.vue'
import _ from 'lodash'
import Vue from 'vue'
import FormDelete from '~/components/comment/FormDelete.vue'
import { Project } from '~/domain/models/project/project'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'
import { CommentListDTO, CommentReadDTO } from '~/services/application/comment/commentData'

export default Vue.extend({
  components: {
    CommentList,
    FormDelete
  },
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      dialogDelete: false,
      project: {} as Project,
      item: {} as CommentListDTO,
      selected: [] as CommentReadDTO[],
      isLoading: false
    }
  },

  async fetch() {
    this.isLoading = true
    this.project = await this.$services.project.findById(this.projectId)
    this.item = await this.$services.comment.listProjectComment(this.projectId, this.$route.query)
    this.isLoading = false
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId() {
      return this.$route.params.id
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  methods: {
    async remove() {
      await this.$services.comment.deleteBulk(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
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
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
