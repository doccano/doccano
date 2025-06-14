<template>
  <v-card class="elevation-0">
    <v-card-title>
      <v-list-item class="grow ps-0">
        <v-list-item-avatar>
          <v-icon large>
            {{ mdiAccountCircle }}
          </v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ comment.username }}</v-list-item-title>
          <v-list-item-subtitle>
            {{
              comment.createdAt | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('DD/MM/YYYY HH:mm')
            }}
          </v-list-item-subtitle>
        </v-list-item-content>

        <v-row align="center" justify="end">
          <v-menu v-if="comment.user == userId" bottom left>
            <template #activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon>{{ mdiDotsVertical }}</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-item>
                <v-list-item-title @click="showEdit = true"> Edit </v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-title @click="$emit('delete-comment', comment)">
                  Delete
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-row>
      </v-list-item>
    </v-card-title>

    <v-card-text class="body-1">
      <span v-if="!showEdit">
        {{ comment.text }}
      </span>
      <v-form v-else v-model="valid">
        <v-row>
          <v-textarea v-model="editText" auto-grow rows="1" solo :rules="commentRules" />
        </v-row>
        <v-row justify="end">
          <v-btn text class="text-capitalize" @click="cancel"> Cancel </v-btn>
          <v-btn
            :disabled="!valid"
            color="primary"
            class="text-capitalize"
            @click="updateComment(editText)"
          >
            Update
          </v-btn>
        </v-row>
      </v-form>
    </v-card-text>
    <v-divider />
  </v-card>
</template>

<script lang="ts">
import { mdiAccountCircle, mdiDotsVertical } from '@mdi/js'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import type { PropType } from 'vue'
import Vue from 'vue'
import { CommentItem } from '~/domain/models/comment/comment'
Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default Vue.extend({
  props: {
    comment: {
      required: true,
      type: Object as PropType<CommentItem>
    },
    userId: {
      required: true,
      type: Number
    }
  },

  data() {
    return {
      showEdit: false,
      editText: this.comment.text,
      commentRules: [(v: string) => !!v.trim() || 'Comment is required'],
      valid: false,
      mdiAccountCircle,
      mdiDotsVertical
    }
  },

  methods: {
    updateComment(newText: string) {
      this.showEdit = false
      const comment = { ...this.comment, text: newText }
      this.$emit('update-comment', comment)
    },

    cancel() {
      this.showEdit = false
      this.editText = this.comment.text
    }
  }
})
</script>
