<template>
  <base-card
    :disabled="!valid"
    :title="$t('user.register')"
    :agree-text="$t('user.register')"
    :cancel-text="$t('cancel')"
    @agree="tryRegister"
    @cancel="cancelRegister"
  >
    <template #content>
      <v-form v-model="valid">
          
        <v-alert v-show="showError" v-model="showError" type="error" dismissible>
          {{ errorMessage }}
        </v-alert>
        <v-text-field
          v-model="username"
          :rules="userNameRules($t('rules.userNameRules'))"
          :label="$t('user.username')"
          name="username"
          :prepend-icon="mdiAccount"
          type="text"
          autofocus
        />
        <v-text-field
          v-model="email"
          :label="$t('user.email')"
          name="email"
          :prepend-icon="mdiEmail"
          type="email"
        />
        <v-text-field
          id="password"
          v-model="password"
          :rules="passwordRules($t('rules.passwordRules'))"
          :label="$t('user.password')"
          name="password"
          :prepend-icon="mdiLock"
          type="password"
        />
        <v-text-field
          id="password2"
          v-model="password2"
          :rules="confirmPasswordRules"
          :label="$t('user.confirmPassword')"
          name="password2"
          :prepend-icon="mdiLock"
          type="password"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiAccount, mdiLock, mdiEmail } from '@mdi/js'
import { userNameRules, passwordRules, emailRules } from '@/rules/index'
import BaseCard from '@/components/utils/BaseCard.vue'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    register: {
      type: Function,
      default: () => Promise
    }
  },
  data() {
    return {
      valid: false,
      username: '',
      email: '',
      password: '',
      password2: '',
      userNameRules,
      passwordRules,
      emailRules,
      showError: false,
      errorMessage: '',
      mdiAccount,
      mdiLock,
      mdiEmail,
    }
  },

  computed: {
    confirmPasswordRules() {
      return [
        (v: string) => !!v || this.$t('rules.passwordRules.required'),
        (v: string) => v === this.password || this.$t('rules.passwordRules.match')
      ]
    }
  },

  methods: {
    async tryRegister() {
      try {
        await this.register({
          username: this.username,
          email: this.email,
          password1: this.password,
          password2: this.password2
        })
        this.$router.push(this.localePath('/users'))
        
      } catch (error: any) {
        this.showError = true
        this.errorMessage = error.message || this.$t('errors.invalidUserOrPass')
      }
    },
    cancelRegister() {
    this.$router.push(this.localePath('/users')) 
  }
  }
})
</script>