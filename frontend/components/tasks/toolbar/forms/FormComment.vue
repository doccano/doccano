<template>
  <base-card
    :title="$t('comments.comments')"
    :cancel-text="$t('generic.close')"
    @cancel="$emit('click:cancel')"
  >
    <template #content>
      <form-create
        @add-comment="add"
      />
      <comment
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :user-id="user.id"
        @delete-comment="remove"
        @update-comment="maybeUpdate"
      />
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import Comment from '@/components/comment/Comment.vue'
import FormCreate from '@/components/comment/FormCreate.vue'
import { CommentReadDTO } from '~/services/application/comment/commentData'

export default Vue.extend({
  components: {
    BaseCard,
    Comment,
    FormCreate
  },

  props: {
    docId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      user: {},
      comments: [] as CommentReadDTO[],
    }
  },

  async fetch() {
    this.user = await this.$services.user.getMyProfile()
  },

  watch: {
    currentDoc: {
      handler(val) {
        if (val !== undefined) {
          this.list()
        }
      },
      immediate: true,
      deep: true
    }
  },

  methods: {
    async list() {
      this.comments = await this.$services.comment.list(this.$route.params.id, this.docId)
    },
    async add(message: string) {
      await this.$services.comment.create(this.$route.params.id, this.docId, message)
      this.list()
    },
    async remove(item: CommentReadDTO) {
      await this.$services.comment.delete(this.$route.params.id, this.docId, item)
      this.list()
    },
    async maybeUpdate(item: CommentReadDTO) {
      await this.$services.comment.update(this.$route.params.id, this.docId, item)
      this.list()
    }
  }
})
</script>
