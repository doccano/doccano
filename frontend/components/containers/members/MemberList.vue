<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="loading"
    loading-text="Loading... Please wait"
    item-key="id"
    show-select
    @input="updateSelected"
  >
    <template v-slot:top>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        label="Search"
        single-line
        hide-details
        filled
      />
    </template>
    <template v-slot:item.role="{ item }">
      <v-edit-dialog
        :return-value.sync="item.role"
        large
        persistent
        @save="updateRole({ id: item.id, role: newRole })"
      >
        <div>{{ item.role }}</div>
        <template v-slot:input>
          <div class="mt-4 title">
            Update Role
          </div>
        </template>
        <template v-slot:input>
          <v-select
            :value="item.role"
            :items="roles"
            :rules="roleRules"
            label="Role"
            @input="setNewRole"
          />
        </template>
      </v-edit-dialog>
    </template>
  </v-data-table>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'
import { roleRules } from '@/rules/index'

export default {
  data() {
    return {
      roles: [
        'Admin',
        'Member'
      ],
      search: '',
      newRole: null,
      roleRules
    }
  },

  computed: {
    ...mapState('members', ['items', 'selected', 'loading']),
    ...mapGetters('members', ['headers'])
  },

  created() {
    this.getMemberList()
  },

  methods: {
    ...mapActions('members', ['getMemberList', 'updateMemberRole']),
    ...mapMutations('members', ['updateSelected']),

    setNewRole(value) {
      this.newRole = value
    },

    updateRole(payload) {
      const data = {
        projectId: this.$route.params.id,
        ...payload
      }
      this.updateMemberRole(data)
    }
  }
}
</script>
