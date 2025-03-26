<template>
  <v-card>
    <v-card-title>{{ selectedUser ? $t('generic.edit') : $t('generic.create') }}</v-card-title>
    <v-card-text>
      <v-form v-model="valid" ref="form">
        <v-text-field v-model="firstName" :label="$t('First Name')" :rules="firstNameRules" required />
        <v-text-field v-model="lastName" :label="$t('Last Name')" :rules="lastNameRules" required />
        <v-text-field v-model="username" :label="$t('Username')" :rules="usernameRules" required />
        <v-text-field v-model="email" :label="$t('Email')" :rules="emailRules" type="email" required />

        <v-text-field
          v-if="!selectedUser"
          v-model="password1"
          :label="$t('Password')"
          :rules="passwordRules"
          type="password"
          required
        />
        <v-text-field
          v-if="!selectedUser"
          v-model="password2"
          :label="$t('Confirm Password')"
          :rules="[v => v === password1 || $t('user.passwordNotMatch')]"
          type="password"
          required
        />

        <v-checkbox v-model="isSuperuser" :label="$t('Superuser')" />
        <v-checkbox v-model="isStaff" :label="$t('Staff')" />
      </v-form>

      <v-alert v-if="errorMessage" type="error" dense>
        {{ errorMessage }}
      </v-alert>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn text @click="$emit('cancel')">{{ $t('generic.cancel') }}</v-btn>
      <v-btn color="primary" :disabled="!valid" :loading="loading" @click="saveUser">
        {{ selectedUser ? $t('generic.update') : $t('generic.save') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    selectedUser: Object
  },
  data() {
    return {
      valid: false,
      loading: false,
      firstName: '',
      lastName: '',
      username: '',
      email: '',
      password1: '',
      password2: '',
      isSuperuser: false,
      isStaff: false,
      errorMessage: '',
      firstNameRules: [(v: string) => !!v || this.$t('First name')],
      lastNameRules: [(v: string) => !!v || this.$t('Last name')],
      usernameRules: [
        (v: string) => !!v || this.$t('User name is required'),
        (v: string) => v.length <= 30 || this.$t('User name is too long')
      ],
      emailRules: [
        (v: string) => !!v || this.$t('User email is required'),
        (v: string) => /.+@.+\..+/.test(v) || this.$t('User email must be valid'),
        (v: string) => v.length <= 254 || this.$t('User email is too long')
      ],
      passwordRules: [
        (v: string) => !!v || this.$t('user.passwordRequired'),
        (v: string) => v.length >= 8 || this.$t('user.passwordTooShort')
      ]
    }
  },
  watch: {
    selectedUser: {
      handler(user) {
        if (user) {
          this.firstName = user.firstName || ''
          this.lastName = user.lastName || ''
          this.username = user.username || ''
          this.email = user.email || ''
          this.isSuperuser = user.isSuperuser || false
          this.isStaff = user.isStaff || false
        } else {
          this.resetForm()
        }
      },
      immediate: true
    }
  },
  methods: {
    resetForm() {
      this.firstName = ''
      this.lastName = ''
      this.username = ''
      this.email = ''
      this.password1 = ''
      this.password2 = ''
      this.isSuperuser = false
      this.isStaff = false
    },
    async saveUser() {
      if (!(this.$refs.form as Vue & { validate: () => boolean }).validate()) {
        return
      }

      this.loading = true
      this.errorMessage = ''

      try {
        if (this.selectedUser) {
          await this.$repositories.user.update(this.selectedUser.id, {
            firstName: this.firstName,
            lastName: this.lastName,
            username: this.username,
            email: this.email,
            is_superuser: this.isSuperuser,
            is_staff: this.isStaff
          })
        } else {
          await this.$repositories.user.create({
            username: this.username,
            email: this.email,
            password1: this.password1,
            password2: this.password2,
            is_superuser: this.isSuperuser,
            is_staff: this.isSuperuser ? true : this.isStaff
          })
        }
        this.$emit('save')
      } catch (e: any) {
        this.errorMessage = e.response?.data?.detail || this.$t('generic.error')
      } finally {
        this.loading = false
      }
    }
  }
})
</script>