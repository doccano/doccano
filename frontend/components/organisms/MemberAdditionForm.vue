<template>
  <base-card
    title="Add Member"
    agree-text="Add"
    cancel-text="Cancel"
    :disabled="!valid"
    @agree="create"
    @cancel="cancel"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-autocomplete
          v-model="selectedUser"
          :items="items"
          :loading="isLoading"
          :search-input.sync="username"
          :rules="userRules"
          color="white"
          hide-no-data
          hide-selected
          item-text="username"
          label="User Search APIs"
          placeholder="Start typing to Search"
          prepend-icon="mdi-account"
          return-object
        />
        <v-select
          v-model="role"
          :items="roles"
          :rules="roleRules"
          label="Role"
          prepend-icon="mdi-account-card-details-outline"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    BaseCard
  },
  props: {
    addMember: {
      type: Function,
      default: () => {},
      required: true
    },
    items: {
      type: Array,
      default: () => {},
      required: true
    }
  },
  data() {
    return {
      valid: false,
      username: '',
      role: null,
      isLoading: false,
      selectedUser: null,
      roles: ['Admin', 'Member'],
      userRules: [
        v => !!v || 'User is required'
      ],
      roleRules: [
        v => !!v || 'Role is required'
      ]
    }
  },

  watch: {
    username(val) {
      this.$emit('search-user', val)
    }
  },

  methods: {
    cancel() {
      this.$emit('close')
    },
    validate() {
      return this.$refs.form.validate()
    },
    reset() {
      this.$refs.form.reset()
    },
    create() {
      if (this.validate()) {
        this.addMember({
          userId: this.selectedUser.id,
          projectId: this.$route.params.id,
          role: this.role
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
