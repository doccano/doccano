<template>
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="comments.toArray()"
    :search="search"
    :options.sync="options"
    :server-items-length="comments.count()"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
  >
    <template v-slot:[`item.created_at`]="{ item }">
      <span>{{ item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD HH:mm') }}</span>
    </template>
    <template v-slot:[`item.document_text`]="{ item }">
      {{ item.document_text | truncate(200) }}
    </template>
    <template v-slot:top>
      <base-modal>
        <template v-slot:opener="modal">
          <v-btn
            :disabled="selected.length === 0"
            class="text-capitalize ma-6"
            outlined
            @click="modal.open"
          >
            {{ $t('generic.delete') }}
          </v-btn>
        </template>
        <template v-slot:content="modal">
          <confirm-form
            :items="selected"
            :title="$t('comments.removeComment')"
            :message="$t('comments.removePrompt')"
            item-key="text"
            @ok="remove();modal.close()"
            @cancel="modal.close"
          />
        </template>
      </base-modal>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
  </v-data-table>
</template>

<script>
import Vue from 'vue'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import { CommentApplicationService } from '@/services/application/comment.service'
import { FromApiCommentItemListRepository } from '@/repositories/comment/api'
import ConfirmForm from '@/components/organisms/utils/ConfirmForm.vue'
import BaseModal from '@/components/atoms/BaseModal.vue'
import { CommentItemList } from '~/models/comment'
Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default {
  components: {
    ConfirmForm,
    BaseModal
  },

  fetch() {
    this.list()
  },

  data() {
    return {
      search: this.$route.query.q,
      comments: CommentItemList.valueOf([]),
      selected: [],
      isLoading: false,
      options: {},
      headers: [
        {
          text: this.$t('comments.created_at'),
          align: 'left',
          value: 'created_at'
        },
        {
          text: this.$t('comments.document'),
          value: 'document_text'
        },
        {
          text: this.$t('user.username'),
          value: 'username'
        },
        {
          text: this.$t('dataset.text'),
          value: 'text'
        }
      ]
    }
  },

  computed: {
    service() {
      const repository = new FromApiCommentItemListRepository()
      return new CommentApplicationService(repository)
    }
  },

  watch: {
    search() {
      this.list()
    }
  },

  methods: {
    async list() {
      this.isLoading = true
      this.comments = await this.service.listProjectComment(this.$route.params.id, this.search)
      this.isLoading = false
    },

    async remove() {
      this.isLoading = true
      const items = CommentItemList.valueOf(this.selected)
      await this.service.deleteBulk(this.$route.params.id, items)
      this.comments.deleteBulk(items)
      this.isLoading = false
    }
  }
}
</script>
