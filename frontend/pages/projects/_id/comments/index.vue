<template>
  <v-card>
    <v-card-title>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete=true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>
    <comment-list
      v-model="selected"
      :examples="examples.items"
      :items="items"
      :is-loading="isLoading"
      @click:labeling="movePage"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import CommentList from '@/components/comment/CommentList.vue'
import { CommentReadDTO } from '~/services/application/comment/commentData'
import { ExampleListDTO } from '~/services/application/example/exampleData'
import { ProjectDTO } from '~/services/application/project/projectData'
import FormDelete from '~/components/comment/FormDelete.vue'

export default Vue.extend({
  layout: 'project',

  components: {
    CommentList,
    FormDelete
  },

  async fetch() {
    this.isLoading = true
    this.project = await this.$services.project.findById(this.projectId)
    this.items = await this.$services.comment.listProjectComment(this.projectId)
    const example = await this.$services.example.fetchOne(this.projectId,'1','','') // to fetch the count of examples
    this.examples = await this.$services.example.list(this.projectId, {limit: example.count.toString()})
    this.isLoading = false
  },

  data() {
    return {
      dialogDelete: false,
      project: {} as ProjectDTO,
      items: [] as CommentReadDTO[],
      selected: [] as CommentReadDTO[],
      examples: {} as ExampleListDTO,
      isLoading: false
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId() {
      return this.$route.params.id
    }
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
      this.updateQuery({
        path: this.localePath(this.project.pageLink),
        query
      })
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
