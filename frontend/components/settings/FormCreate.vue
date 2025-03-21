<template>
  <v-card>
    <v-card-title>{{ $t('generic.create') }}</v-card-title>
    <v-card-text>
      <v-form v-model="valid" ref="form">
        <v-text-field
          v-model="username"
          :label="$t('Username')"
          :rules="usernameRules"
          required
        />
        <v-text-field
          v-model="email"
          :label="$t('Email')"
          :rules="emailRules"
          type="email"
          required
        />
        <v-text-field
          v-model="password1"
          :label="$t('Password')"
          :rules="passwordRules"
          type="password"
          required
        />
        <v-text-field
          v-model="password2"
          :label="$t('Confirm Password')"
          :rules="[v => v === password1 || $t('user.passwordNotMatch')]"
          type="password"
          required
        />
      </v-form>
      <v-alert v-if="errorMessage" type="error" dense>{{ errorMessage }}</v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="$emit('cancel')">{{ $t('generic.cancel') }}</v-btn>
      <v-btn
        color="primary"
        :disabled="!valid"
        :loading="loading"
        @click="create"
      >{{ $t('generic.save') }}</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      valid: false,
      loading: false,
      username: '',
      email: '',
      password1: '',
      password2: '',
      errorMessage: '',
      usernameRules: [
        (v: string) => !!v || this.$t('user.usernameRequired'),
        (v: string) => v.length <= 30 || this.$t('user.usernameTooLong')
      ],
      emailRules: [
        (v: string) => !!v || this.$t('user.emailRequired'),
        (v: string) => /.+@.+\..+/.test(v) || this.$t('user.emailInvalid')
      ],
      passwordRules: [
        (v: string) => !!v || this.$t('user.passwordRequired'),
        (v: string) => v.length >= 8 || this.$t('user.passwordTooShort')
      ]
    }
  },

  methods: {
    async create() {
      if (!(this.$refs.form as Vue & { validate: () => boolean }).validate()) {
        return
      }
      this.loading = true
      this.errorMessage = ''
      try {
        await this.$services.user.create({
          username: this.username,
          email: this.email,
          password1: this.password1,
          password2: this.password2
        })
        this.$emit('save')
      } catch (e) {
        this.errorMessage = e.response.data.detail || this.$t('generic.error')
      } finally {
        this.loading = false
      }
    }
  }
})
</script>