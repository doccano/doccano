<template>
  <div>
    <div class="font-weight-bold ml-8 mb-2">
      {{ this.$t('comments.comments') }}
    </div>

    <v-timeline
      align-top
      dense
    >
      <v-timeline-item
        fill-dot
        class="mb-12"
        color="green"
        large
      >
        <v-textarea
          v-model="message"
          outlined
          name="CommentInput"
          :label="this.$t('comments.message')"
          value=""
        />
        <v-btn
          class="white--text"
          color="green"
          depressed
          :disabled="message.length === 0"
          @click="add"
        >
          {{ this.$t('comments.send') }}
        </v-btn>
      </v-timeline-item>
      <comment
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :user-id="userId"
        @delete-comment="remove"
        @update-comment="update"
      />
    </v-timeline>
  </div>
</template>

<script>

import { mapActions, mapState, mapMutations } from 'vuex'
import Comment from './Comment'

export default {
  name: 'CommentSection',
  components: { Comment },
  fetch() {
    this.getMyUserId()
  },
  data() {
    return {
      message: ''
    }
  },
  computed: {
    ...mapState('documents', ['items', 'total', 'current', 'selected']),
    ...mapState('comments', ['comments', 'userId'])
  },
  watch: {
    total() {
      this.getCommentList({
        projectId: this.$route.params.id,
        docId: this.items[this.current].id
      })
    },
    current: {
      handler() {
        if (this.total !== 0) {
          this.getCommentList({
            projectId: this.$route.params.id,
            docId: this.items[this.current].id
          })
        }
      },
      immediate: true
    }
  },
  methods: {
    add() {
      this.addComment({
        text: this.message,
        projectId: this.$route.params.id,
        docId: this.items[this.current].id
      })
      this.message = ''
    },
    remove(comment) {
      this.updateSelectedComments([comment])
      this.deleteComment({
        projectId: this.$route.params.id,
        docId: this.items[this.current].id
      })
    },
    update(commentId, text) {
      this.updateComment({
        projectId: this.$route.params.id,
        docId: this.items[this.current].id,
        commentId,
        text
      })
    },
    ...mapActions('comments', ['addComment', 'getCommentList', 'deleteComment', 'updateComment', 'getMyUserId']),
    ...mapMutations('comments', ['updateSelectedComments'])
  }
}

</script>
