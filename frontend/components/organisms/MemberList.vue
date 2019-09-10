<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="members"
    :search="search"
    :loading="loading"
    loading-text="Loading... Please wait"
    item-key="id"
    show-select
    @input="update"
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
import { roleRules } from '@/rules/index'

export default {
  props: {
    headers: {
      type: Array,
      default: () => [],
      required: true
    },
    members: {
      type: Array,
      default: () => [],
      required: true
    },
    selected: {
      type: Array,
      default: () => [],
      required: true
    },
    roles: {
      type: Array,
      default: () => [
        'Admin',
        'Member'
      ]
    },
    loading: {
      type: Boolean,
      default: false,
      required: true
    }
  },
  data() {
    return {
      search: '',
      newRole: null,
      roleRules
    }
  },
  methods: {
    setNewRole(value) {
      this.newRole = value
    },
    update(selected) {
      this.$emit('update-selected', selected)
    },
    updateRole(payload) {
      this.$emit('update-role', payload)
    }
  }
}
</script>
