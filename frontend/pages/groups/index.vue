<template>
  <v-card>
    <v-card-title v-if="isStaff">
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        class="text-capitalize ms-2"
        color="primary"
        outlined
        @click="dialogCreate = true"
      >
        {{ $t('generic.create') }}
      </v-btn>
      <v-dialog v-model="dialogDelete" max-width="500">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
      <v-dialog v-model="dialogCreate" max-width="800">
        <form-create @cancel="dialogCreate = false" @created="handleCreated" />
      </v-dialog>
    </v-card-title>
    <group-list
      v-model="selected"
      :items="groups"
      :is-loading="isLoading"
      :total="total"
      @update:query="updateQuery"
    />
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import GroupList from '@/components/groups/GroupList.vue'
import FormDelete from '@/components/groups/FormDelete.vue'
import FormCreate from '@/components/groups/FormCreate.vue'
import { Group } from '@/domain/models/group/group'

export default Vue.extend({
  components: {
    GroupList,
    FormDelete,
    FormCreate
  },
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogDelete: false,
      dialogCreate: false,
      groups: [] as Group[],
      selected: [] as Group[],
      isLoading: false,
      total: 0
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      const query = this.buildQuery()
      const list = await this.$services.group.listGroups(query)
      this.groups = list.results
      this.total = list.count
    } catch (e) {
      this.$store.dispatch('notification/setNotification', {
        color: 'error',
        text: 'Failed to load groups'
      })
    } finally {
      this.isLoading = false
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 500)
  },

  methods: {
    buildQuery() {
      const { q, limit, offset, ordering, orderBy } = this.$route.query
      const params = new URLSearchParams()
      
      if (q) params.append('search', q as string)
      if (limit) params.append('limit', limit as string)
      if (offset) params.append('offset', offset as string)
      
      if (ordering && orderBy) {
        const direction = orderBy === '-' ? '-' : ''
        params.append('ordering', `${direction}${ordering}`)
      }
      
      return params.toString()
    },

    async remove() {
      try {
        for (const group of this.selected) {
          await this.$services.group.deleteGroup(group.id)
        }
        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: 'Groups deleted successfully'
        })
        this.$fetch()
      } catch (e) {
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Failed to delete groups'
        })
      } finally {
        this.dialogDelete = false
        this.selected = []
      }
    },

    updateQuery(query: { query: Record<string, string> }) {
      this.$router.push({
        query: {
          ...query.query
        }
      })
    },

    handleCreated() {
      this.dialogCreate = false
      this.$fetch()
      this.$store.dispatch('notification/setNotification', {
        color: 'success',
        text: 'Group created successfully'
      })
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
