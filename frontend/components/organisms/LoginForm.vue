<template>
  <v-card class="elevation-12">
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>Login</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-text-field
          v-model="username"
          :rules="userNameRules"
          label="Login"
          name="login"
          prepend-icon="person"
          type="text"
        />
        <v-text-field
          id="password"
          v-model="password"
          :rules="passwordRules"
          label="Password"
          name="password"
          prepend-icon="lock"
          type="password"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <div class="flex-grow-1" />
      <v-btn
        :disabled="!valid"
        color="primary"
        @click="tryLogin"
      >
        Login
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { userNameRules, passwordRules } from '@/rules/index'

export default {
  props: {
    login: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      valid: false,
      username: '',
      password: '',
      userNameRules,
      passwordRules
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
    tryLogin() {
      if (this.validate()) {
        this.login({
          username: this.username,
          password: this.password
        })
        this.reset()
        this.cancel()
      }
    }
  }
}
</script>
