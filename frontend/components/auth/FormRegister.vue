<template>
  <base-card
    :disabled="!valid || !isDatabaseHealthy"
    :title="$t('user.register')"
    :agree-text="$t('user.register')"
    :cancel-text="$t('generic.cancel')"
    @agree="tryRegister"
    @cancel="cancelRegister"
  >
    <template #content>
      <v-form v-model="valid" :disabled="!isDatabaseHealthy">
        <v-alert v-show="showError" v-model="showError" type="error" dismissible>
          {{ errorMessage }}
        </v-alert>
        <v-alert v-show="showSuccess" v-model="showSuccess" type="success" dismissible>
          {{ successMessage }}
        </v-alert>
        <v-alert v-show="!isDatabaseHealthy" type="error" class="mb-4">
          {{ databaseMessage }}
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
          v-model="firstName"
          :rules="firstNameRules"
          label="Nome"
          name="firstName"
          :prepend-icon="mdiAccount"
          type="text"
        />
        <v-text-field
          v-model="lastName"
          :rules="lastNameRules"
          label="Apelido"
          name="lastName"
          :prepend-icon="mdiAccount"
          type="text"
        />
        <v-text-field
          v-model="email"
          :rules="emailRules($t('rules.emailRules'))"
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
          id="passwordConfirm"
          v-model="passwordConfirm"
          :rules="confirmPasswordRules"
          :label="$t('user.confirmPassword')"
          name="passwordConfirm"
          :prepend-icon="mdiLock"
          type="password"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiAccount, mdiLock, mdiEmail, mdiDatabaseAlert } from '@mdi/js'
import { userNameRules, passwordRules, emailRules } from '@/rules/index'
import BaseCard from '@/components/utils/BaseCard.vue'
import { databaseHealthMixin } from '@/mixins/databaseHealthMixin'

export default Vue.extend({
  components: {
    BaseCard
  },

  mixins: [databaseHealthMixin],

  props: {
    register: {
      type: Function,
      default: () => () => Promise.resolve()
    }
  },
  data() {
    return {
      valid: false,
      username: '',
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      passwordConfirm: '',
      userNameRules,
      passwordRules,
      emailRules,
      firstNameRules: [(v: string) => !!v || 'Nome é obrigatório'],
      lastNameRules: [(v: string) => !!v || 'Apelido é obrigatório'],
      showError: false,
      errorMessage: '',
      showSuccess: false,
      successMessage: '',
      mdiAccount,
      mdiLock,
      mdiEmail,
      mdiDatabaseAlert
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
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email,
          password: this.password,
          passwordConfirm: this.passwordConfirm
        })
        
        // Mostrar mensagem de sucesso
        this.showError = false
        this.showSuccess = true
        this.successMessage = `Utilizador "${this.username}" criado com sucesso!`
        
        // Redirecionar após 3 segundos
        setTimeout(() => {
        this.$router.push(this.localePath('/users'))
        }, 3000)
        
      } catch (error: any) {
        this.showError = true
        this.showSuccess = false
        this.errorMessage = error.message || 'Erro ao registar utilizador. Verifique os dados inseridos.'
      }
    },
    
    cancelRegister() {
      this.$router.go(-1)
    }
  }
})
</script>