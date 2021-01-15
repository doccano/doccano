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
        :title="$t('annotation.commentPopupTitle')"
        :cancel-text="$t('generic.close')"
        @cancel="dialog=false"
      >
        <template #content>
          <v-text-field
            v-model="comment"
            outlined
          >
            <template
              v-slot:append
            >
              <v-btn
                tile
                large
                icon
                height="auto"
                width="auto"
                color="primary"
                class="ma-0"
                @click="addItem"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
          </v-text-field>
          <v-data-table
            :headers="headers"
            :items="currentDoc.comments"
            :items-per-page="10"
            class="elevation-1"
          >
            <template v-slot:item.action="{ item }">
              <v-icon
                small
                @click="deleteItem(item.id)"
              >
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:item.text="props">
              <v-edit-dialog
                large
                persistent
                @save="editItem"
                @open="openEdit(props.item)"
              >
                <div>{{ props.item.text }}</div>
                <template v-slot:input>
                  <div class="mt-4 title">
                    Update Comment
                  </div>
                  <v-text-field
                    v-model="editedComment.text"
                    label="Edit"
                    single-line
                    counter
                    autofocus
                  />
                </template>
              </v-edit-dialog>
            </template>
          </v-data-table>
        </template>
      </base-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    BaseCard
  },

  data() {
    return {
      dialog: false,
      comment: '',
      editedComment: {
        text: '',
        id: null
      }
    }
  },

  computed: {
    ...mapGetters('documents', ['currentDoc']),
    headers() {
      return [
        {
          text: 'Comments',
          align: 'start',
          sortable: false,
          value: 'text'
        },
        { text: 'Action', value: 'action', sortable: false }
      ]
    }
  },

  methods: {
    ...mapActions('documents', ['addComment', 'deleteComment', 'updateComment']),
    addItem() {
      if (this.comment === '') {
        return
      }
      const payload = {
        text: this.comment,
        projectId: this.$route.params.id
      }
      this.addComment(payload)
      this.comment = ''
    },
    deleteItem(id) {
      const payload = {
        commentId: id,
        projectId: this.$route.params.id
      }
      this.deleteComment(payload)
    },
    editItem() {
      if (this.editedComment.text === '') {
        this.deleteItem(this.editedComment.id)
      } else {
        this.updateComment({
          projectId: this.$route.params.id,
          commentId: this.editedComment.id,
          text: this.editedComment.text
        })
      }
    },
    openEdit(item) {
      Object.assign(this.editedComment, item)
    }
  }
}
</script>
