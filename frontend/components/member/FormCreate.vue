<template>
  <base-card
    :disabled="!valid"
    :title="$t('members.addMember')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('save')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form v-model="valid">
        <v-autocomplete
          v-model="user"
          :items="users"
          :loading="isLoading"
          :search-input.sync="username"
          hide-no-data
          item-text="username"
          :label="$t('members.userSearchAPIs')"
          :placeholder="$t('members.userSearchPrompt')"
          prepend-icon="mdi-account"
          :rules="[rules.userRequired]"
          return-object
        />
        <v-select
          v-model="role"
          :items="roles"
          item-text="rolename"
          item-value="id"
          :label="$t('members.role')"
          :rules="[rules.roleRequired]"
          return-object
          prepend-icon="mdi-credit-card-outline"
        >
          <template v-slot:item="props">
            {{ $translateRole(props.item.rolename, $t('members.roles')) }}
          </template>
          <template v-slot:selection="props">
            {{ $translateRole(props.item.rolename, $t('members.roles')) }}
          </template>
        </v-select>
        <v-alert
          v-show="errorMessage"
          prominent
          type="error"
        >
          <v-row align="center">
            <v-col class="grow">
              {{ errorMessage }}
            </v-col>
          </v-row>
        </v-alert>
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { UserDTO } from '~/services/application/user/userData'
import { RoleDTO } from '~/services/application/role/roleData'
import { MemberDTO } from '~/services/application/member/memberData'

export default Vue.extend({
  components: {
    BaseCard
  },
  
  props: {
    value: {
      type: Object as PropType<MemberDTO>,
      required: true
    },
    errorMessage: {
      type: String,
      default: ''
    }
  },

  async fetch() {
    this.isLoading = true
    this.users = await this.$services.user.list(this.username)
    this.isLoading = false
  },

  data() {
    return {
      isLoading: false,
      valid: false,
      users: [] as UserDTO[],
      roles: [] as RoleDTO[],
      username: '',
      rules: {
        userRequired: (v: UserDTO) => !!v && !!v.username || 'Required',
        roleRequired: (v: RoleDTO) => !!v && !!v.rolename || 'Required'
      }
    }
  },

  computed: {
    user: {
      get(): UserDTO {
        return {
          id: this.value.user,
          username: this.value.username,
          isStaff: false
        }
      },
      set(val: MemberDTO) {
        if (val === undefined) return
        const user = { user: val.id, username: val.username }
        this.$emit('input', { ...this.value, ...user })
      }
    },
    role: {
      get(): RoleDTO {
        return {
          id: this.value.role,
          rolename: this.value.rolename
        }
      },
      set(val: MemberDTO) {
        const role = { role: val.id, rolename: val.rolename }
        this.$emit('input', { ...this.value, ...role })
      }
    }
  },

  watch: {
    username() {
      // Items have already been loaded
      if (this.users.length > 0) return

      // Items have already been requested
      if (this.isLoading) return

      this.$fetch()
    }
  },

  async created() {
    this.roles = await this.$services.role.list()
  }
})
</script>
