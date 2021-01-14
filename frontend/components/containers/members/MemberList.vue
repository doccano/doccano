<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="loading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, $t('generic.all')],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="updateSelected"
  >
    <template v-slot:top>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template v-slot:item.rolename="{ item }">
      <v-edit-dialog
        :return-value.sync="item"
        large
        @save="updateRole({ id: item.id })"
      >
        <div>{{ translateRole(item.rolename, $t('members.roles')) }}</div>
        <template v-slot:input>
          <div class="mt-4 title">
            {{ $t('members.updateRole') }}
          </div>
        </template>
        <template v-slot:input>
          <v-select
            :value="getRole(item)"
            :items="roles"
            :rules="roleRules($t('rules.roleRules'))"
            item-text="name"
            item-value="id"
            :label="$t('members.role')"
            return-object
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
import { translateRole } from '~/plugins/utils'

export default {
  data() {
    return {
      headers: [
        {
          text: this.$t('generic.name'),
          align: 'left',
          sortable: false,
          value: 'username'
        },
        {
          text: this.$t('members.role'),
          value: 'rolename'
        }
      ],
      search: '',
      newRole: null,
      roleRules
    }
  },

  computed: {
    ...mapState('members', ['items', 'selected', 'loading']),
    ...mapGetters('roles', ['roles'])
  },

  created() {
    this.getMemberList({
      projectId: this.$route.params.id
    })
    this.getRoleList()
  },

  methods: {
    ...mapActions('members', ['getMemberList', 'updateMemberRole']),
    ...mapMutations('members', ['updateSelected']),
    ...mapActions('roles', ['getRoleList']),

    getRole(item) {
      return {
        id: item.role,
        userId: item.user,
        mappingId: item.id
      }
    },

    setNewRole(value) {
      this.newRole = value
    },

    updateRole(payload) {
      this.updateMemberRole({
        projectId: this.$route.params.id,
        id: payload.id,
        role: this.newRole.id
      })
    },

    translateRole(role, mappings) {
      return translateRole(role, mappings)
    }
  }
}
</script>
