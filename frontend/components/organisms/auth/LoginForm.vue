<template>
  <base-card
    title="Login"
    agree-text="Login"
    :disabled="!valid"
    @agree="tryLogin"
  >
    <template #content>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-alert
          v-show="showError"
          v-model="showError"
          type="error"
          dismissible
        >
          Incorrect username or password.
        </v-alert>
        <v-text-field
          v-model="username"
          :rules="userNameRules"
          label="Username"
          name="username"
          prepend-icon="person"
          type="text"
          autofocus
          @keyup.enter="tryLogin"
        />
        <v-text-field
          id="password"
          v-model="password"
          :rules="passwordRules"
          label="Password"
          name="password"
          prepend-icon="lock"
          type="password"
          @keyup.enter="tryLogin"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import { userNameRules, passwordRules } from '@/rules/index'
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    BaseCard
  },

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
      passwordRules,
      showError: false
    }
  },

  methods: {
    validate() {
      return this.$refs.form.validate()
    },
    tryLogin() {
      if (this.validate()) {
        this.login({
          username: this.username,
          password: this.password
        })
          .then((result) => {
            this.$router.push('/projects')
          })
          .catch(() => {
            this.showError = true
          })
      }
    }
  }
}
</script>
