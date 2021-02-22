<template>
  <div style="display:inline;">
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          class="text-capitalize ps-1 pe-1"
          min-width="36"
          icon
          v-on="on"
          @click="dialog=true"
        >
          <v-icon>
            mdi-chat
          </v-icon>
        </v-btn>
      </template>
      <span>{{ $t('annotation.commentTooltip') }}</span>
    </v-tooltip>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <base-card
        :title="$t('comments.comments')"
        :cancel-text="$t('generic.close')"
        @cancel="dialog=false"
      >
        <template #content>
          <v-form>
            <v-textarea
              v-model="message"
              auto-grow
              hide-details
              outlined
              rows="1"
              name="CommentInput"
              :label="$t('comments.message')"
            />
            <v-btn
              class="white--text text-capitalize mt-3"
              color="primary"
              depressed
              :disabled="message.length === 0"
              @click="add"
            >
              {{ $t('comments.send') }}
            </v-btn>
          </v-form>
          <comment
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            :user-id="userId"
            @delete-comment="remove"
            @update-comment="update"
          />
        </template>
      </base-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapState, mapMutations } from 'vuex'
import BaseCard from '@/components/molecules/BaseCard'
import Comment from './Comment'

export default {
  components: {
    BaseCard,
    Comment
  },
  fetch() {
    this.getMyUserId()
  },
  data() {
    return {
      dialog: false,
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
