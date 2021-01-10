<template>
  <base-card
    :disabled="!valid"
    :title="$t('user.login')"
    :agree-text="$t('user.login')"
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
          {{ $t('errors.invalidUserOrPass') }}
        </v-alert>
        <v-text-field
          v-model="username"
          :rules="userNameRules($t('rules.userNameRules'))"
          :label="$t('user.username')"
          name="username"
          prepend-icon="person"
          type="text"
          autofocus
          @keyup.enter="tryLogin"
        />
        <v-text-field
          id="password"
          v-model="password"
          :rules="passwordRules($t('rules.passwordRules'))"
          :label="$t('user.password')"
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
            this.$router.push(this.localePath('/projects'))
          })
          .catch(() => {
            this.showError = true
          })
      }
    }
  }
}
</script>
