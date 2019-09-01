<template>
  <base-card title="Add Member">
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
          label="Role"
          prepend-icon="mdi-account-card-details-outline"
        />
      </v-form>
    </template>
    <template #actions>
      <v-btn
        class="text-capitalize"
        text
        color="primary"
        data-test="cancel-button"
        @click="cancel"
      >
        Cancel
      </v-btn>
      <v-btn
        :disabled="!valid"
        class="text-none"
        text
        data-test="create-button"
        @click="create"
      >
        Add
      </v-btn>
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
      valid: true,
      username: '',
      role: null,
      isLoading: false,
      selectedUser: null,
      roles: ['Admin', 'Member']
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
