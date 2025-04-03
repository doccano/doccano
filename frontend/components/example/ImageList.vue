<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :options.sync="options"
    :server-items-length="total"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
      'items-per-page-options': [10, 50, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template #top>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search') + ' (e.g. label:positive)'"
        single-line
        hide-details
        filled
      />
    </template>
    <template #[`item.isConfirmed`]="{ item: row }">
      <v-chip :color="row.isConfirmed ? 'success' : 'warning'" text small>
        {{ row.isConfirmed ? 'Finished' : 'In progress' }}
      </v-chip>
    </template>
    <template #[`item.url`]="{ item: row }">
      <v-img
        :src="row.url"
        aspect-ratio="1"
        height="150"
        max-height="150"
        width="150"
        class="grey lighten-2"
      />
    </template>
    <template #[`item.meta`]="{ item: row }">
      {{ JSON.stringify(row.meta, null, 4) }}
    </template>
    <template #[`item.assignee`]="{ item: row }">
      <v-combobox
        :value="toSelected(row)"
        :items="members"
        item-text="username"
        no-data-text="No one"
        multiple
        chips
        dense
        flat
        hide-selected
        hide-details
        small-chips
        solo
        style="width: 200px"
        @change="onAssignOrUnassign(row, $event)"
      >
        <template #selection="{ attrs, item: selectedItem, parent, selected }">
          <v-chip v-bind="attrs" :input-value="selected" small class="mt-1 mb-1">
            <span class="pr-1">{{ selectedItem.username }}</span>
            <v-icon small @click="parent.selectItem(selectedItem)"> $delete </v-icon>
          </v-chip>
        </template>
      </v-combobox>
    </template>
    <template #[`item.action`]="{ item: row }">
      <v-btn small color="primary text-capitalize" @click="toLabeling(row)">
        {{ $t('dataset.annotate') }}
      </v-btn>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { ExampleDTO } from '~/services/application/example/exampleData'
import { MemberItem } from '~/domain/models/member/member'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    },
    members: {
      type: Array as PropType<MemberItem[]>,
      default: () => [],
      required: true
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      search: this.$route.query.q,
      options: {} as DataOptions,
      mdiMagnify
    }
  },

  computed: {
    headers() {
      const headers = [
        {
          text: 'Status',
          value: 'isConfirmed',
          sortable: false
        },
        {
          text: 'Image',
          value: 'url',
          sortable: false
        },
        {
          text: 'Filename',
          value: 'filename',
          sortable: false
        },
        {
          text: this.$t('dataset.metadata'),
          value: 'meta',
          sortable: false
        },
        {
          text: this.$t('dataset.action'),
          value: 'action',
          sortable: false
        }
      ]
      if (this.isAdmin) {
        headers.splice(4, 0, {
          text: 'Assignee',
          value: 'assignee',
          sortable: false
        })
      }
      return headers
    }
  },

  watch: {
    options: {
      handler() {
        this.$emit('update:query', {
          query: {
            limit: this.options.itemsPerPage.toString(),
            offset: ((this.options.page - 1) * this.options.itemsPerPage).toString(),
            q: this.search
          }
        })
      },
      deep: true
    },
    search() {
      this.$emit('update:query', {
        query: {
          limit: this.options.itemsPerPage.toString(),
          offset: '0',
          q: this.search
        }
      })
      this.options.page = 1
    }
  },

  methods: {
    toLabeling(record: ExampleDTO) {
      const index = this.items.indexOf(record)
      const offset = (this.options.page - 1) * this.options.itemsPerPage
      const page = (offset + index + 1).toString()
      this.$emit('click:labeling', { page, q: this.search })
    },

    toSelected(record: ExampleDTO) {
      const assigneeIds = record.assignments.map((assignment) => assignment.assignee_id)
      return this.members.filter((member) => assigneeIds.includes(member.user))
    },

    onAssignOrUnassign(record: ExampleDTO, newAssignees: MemberItem[]) {
      const newAssigneeIds = newAssignees.map((assignee) => assignee.user)
      const oldAssigneeIds = record.assignments.map((assignment) => assignment.assignee_id)
      if (oldAssigneeIds.length > newAssigneeIds.length) {
        // unassign
        for (const assignment of record.assignments) {
          if (!newAssigneeIds.includes(assignment.assignee_id)) {
            this.$emit('unassign', assignment.id)
          }
        }
      } else {
        // assign
        for (const newAssigneeId of newAssigneeIds) {
          if (!oldAssigneeIds.includes(newAssigneeId)) {
            this.$emit('assign', record.id, newAssigneeId)
          }
        }
      }
    }
  }
})
</script>
