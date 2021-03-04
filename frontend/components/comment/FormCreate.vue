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
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            :user-id="user.id"
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
import { mapGetters } from 'vuex'
import BaseCard from '@/components/molecules/BaseCard.vue'
import { CommentItem } from '@/models/comment'
import Comment from './Comment.vue'
import { CommentReadDTO } from '~/services/application/comment.service'

export default Vue.extend({
  components: {
    BaseCard,
    Comment
  },

  async fetch() {
    this.user = await this.$services.user.getMyProfile()
  },

  data() {
    return {
      dialog: false,
      user: {},
      comments: [] as CommentReadDTO[],
      commentRules: [
        (v: string) => !!v.trim() || 'Comment is required'
      ],
      message: '',
      valid: false
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
    async add() {
      await this.$services.comment.create(this.$route.params.id, this.currentDoc.id, this.message)
      this.list()
      this.message = ''
    },
    async remove(item: CommentItem) {
      await this.$services.comment.delete(this.$route.params.id, this.currentDoc.id, item)
      this.list()
    },
    async maybeUpdate(item: CommentItem) {
      await this.$services.comment.update(this.$route.params.id, this.currentDoc.id, item)
      this.list()
    }
  }
})
</script>
