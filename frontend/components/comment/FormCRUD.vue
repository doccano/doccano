<template>
  <base-card
    :title="$t('comments.comments')"
    :cancel-text="$t('generic.close')"
    @cancel="$emit('cancel')"
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
import { mapGetters } from 'vuex'
import BaseCard from '@/components/utils/BaseCard.vue'
import Comment from './Comment.vue'
import FormCreate from './FormCreate.vue'
import { CommentReadDTO } from '~/services/application/comment.service'

export default Vue.extend({
  components: {
    BaseCard,
    Comment,
    FormCreate
  },

  async fetch() {
    this.user = await this.$services.user.getMyProfile()
  },

  data() {
    return {
      user: {},
      comments: [] as CommentReadDTO[],
    }
  },

  computed: {
    ...mapGetters('documents', ['currentDoc'])
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
      this.comments = await this.$services.comment.list(this.$route.params.id, this.currentDoc.id)
    },
    async add(message: string) {
      await this.$services.comment.create(this.$route.params.id, this.currentDoc.id, message)
      this.list()
    },
    async remove(item: CommentReadDTO) {
      await this.$services.comment.delete(this.$route.params.id, this.currentDoc.id, item)
      this.list()
    },
    async maybeUpdate(item: CommentReadDTO) {
      await this.$services.comment.update(this.$route.params.id, this.currentDoc.id, item)
      this.list()
    }
  }
})
</script>
