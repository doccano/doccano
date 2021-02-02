<template>
  <div>
    <v-timeline-item
      small
    >
      <div class="font-weight-normal">
        <strong>{{ comment.username }}</strong> @{{ comment.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD HH:mm') }}
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-if="comment.user == userId"
              icon
              color="green"
              v-bind="attrs"
              v-on="on"
              @click="showEdit=true"
            >
              <v-icon>mdi-comment-edit-outline</v-icon>
            </v-btn>
          </template>
          <span>Edit Comment</span>
        </v-tooltip>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-if="comment.user == userId"
              icon
              color="red"
              v-bind="attrs"
              v-on="on"
              @click="$emit('delete-comment', comment)"
            >
              <v-icon>mdi-delete-outline</v-icon>
            </v-btn>
          </template>
          <span>Delete Comment</span>
        </v-tooltip>
      </div>
      <div v-if="!showEdit">
        {{ comment.text }}
      </div>
      <div v-else>
        <v-textarea
          v-model="editText"
          solo
        />
        <div>
          <v-btn
            color="red"
            @click="showEdit=false"
          >
            Close
          </v-btn>
          <v-btn
            color="green"
            @click="updateComment(editText)"
          >
            Update
          </v-btn>
        </div>
      </div>
    </v-timeline-item>
  </div>
</template>

<script>

import Vue from 'vue'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default {
  name: 'Comment',
  props: {
    comment: {
      required: true,
      type: Object
    },
    userId: {
      required: true,
      type: Number
    }
  },
  data() {
    return {
      showEdit: false,
      editText: this.comment.text
    }
  },
  methods: {
    updateComment(newText) {
      this.showEdit = false
      this.$emit('update-comment', this.comment.id, newText)
    }
  }
}
</script>
