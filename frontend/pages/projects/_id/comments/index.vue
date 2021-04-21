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
      :items="items"
      :is-loading="isLoading"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import CommentList from '@/components/comment/CommentList.vue'
import { CommentReadDTO } from '~/services/application/comment/commentData'
import FormDelete from '~/components/comment/FormDelete.vue'

export default Vue.extend({
  layout: 'project',

  components: {
    CommentList,
    FormDelete
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.comment.listProjectComment(this.projectId)
    this.isLoading = false
  },

  data() {
    return {
      dialogDelete: false,
      items: [] as CommentReadDTO[],
      selected: [] as CommentReadDTO[],
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
