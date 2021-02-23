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
          <v-form v-model="valid">
            <v-textarea
              v-model="message"
              auto-grow
              hide-details
              outlined
              rows="1"
              name="CommentInput"
              :label="$t('comments.message')"
              :rules="commentRules"
            />
            <v-btn
              class="white--text text-capitalize mt-3"
              color="primary"
              depressed
              :disabled="!valid"
              @click="add"
            >
              {{ $t('comments.send') }}
            </v-btn>
          </v-form>
          <comment
            v-for="comment in comments.toArray()"
            :key="comment.id"
            :comment="comment"
            :user-id="userId"
            @delete-comment="remove"
            @update-comment="maybeUpdate"
          />
        </template>
      </base-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapActions, mapState, mapGetters } from 'vuex'
import BaseCard from '@/components/molecules/BaseCard.vue'
import { CommentApplicationService } from '@/services/application/comment.service'
import { FromApiCommentItemListRepository } from '@/repositories/comment/api'
import { CommentItem, CommentItemList } from '@/models/comment'
import Comment from './Comment.vue'

export default Vue.extend({
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
      comments: CommentItemList.valueOf([]),
      commentRules: [
        (v: string) => !!v.trim() || 'Comment is required'
      ],
      message: '',
      valid: false
    }
  },

  computed: {
    ...mapGetters('documents', ['currentDoc']),
    ...mapState('comments', ['userId']),
    service() {
      const repository = new FromApiCommentItemListRepository()
      const service = new CommentApplicationService(repository)
      return service
    }
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
      this.comments = await this.service.list(this.$route.params.id, this.currentDoc.id)
    },
    async add() {
      const item = await this.service.create(this.$route.params.id, this.currentDoc.id, this.message)
      this.comments.add(item)
      this.message = ''
    },
    async remove(item: CommentItem) {
      await this.service.delete(this.$route.params.id, this.currentDoc.id, item)
      this.comments.delete(item)
    },
    async maybeUpdate(item: CommentItem) {
      const comment = await this.service.update(this.$route.params.id, this.currentDoc.id, item)
      this.comments.update(comment)
    },
    ...mapActions('comments', ['getMyUserId'])
  }
})
</script>
