<template>
    <v-card>
      <v-card-title>{{ $t('generic.create') }}</v-card-title>
      <v-card-text>
        <v-form v-model="valid" ref="form">
          <!-- Novos campos First name e Last name -->
          <v-text-field
            v-model="firstName"
            :label="$t('First Name')"
            :rules="firstNameRules"
            required
          />
          <v-text-field
            v-model="lastName"
            :label="$t('Last Name')"
            :rules="lastNameRules"
            required
          />
          <v-text-field
            v-model="username"
            :label="$t('Username')"
            :rules="usernameRules"
            required
          />
          <v-text-field
            v-model="first_name"
            :label="$t('First Name')"
            :rules="nameRules"
            required
            />
          <v-text-field
            v-model="last_name"
            :label="$t('Last Name')"
            :rules="nameRules"
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
          <!-- Checkbox para Superuser -->
          <v-checkbox
            v-model="isSuperuser"
            :label="$t('Superuser - If selected, this option grants the user full privileges automatically')"
          />
          <!-- Checkbox para Staff -->
          <v-checkbox
            v-model="isStaff"
            :label="$t('Staff - If selected, the user will have staff status without full privileges')"
          />
        </v-form>
        <v-alert v-if="errorMessage" type="error" dense>
          {{ errorMessage }}
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('cancel')">{{ $t('generic.cancel') }}</v-btn>
        <v-btn
          color="primary"
          :disabled="!valid"
          :loading="loading"
          @click="create"
        >
          {{ $t('generic.save') }}
        </v-btn>
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
        firstName: '',
        lastName: '',
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password1: '',
        password2: '',
        isSuperuser: false,
        isStaff: false,
        errorMessage: '',
        firstNameRules: [
          (v: string) => !!v || this.$t('First name')
        ],
        lastNameRules: [
          (v: string) => !!v || this.$t('Last name')
        ],
        usernameRules: [
          (v: string) => !!v || this.$t('User name is required'),
          (v: string) => v.length <= 30 || this.$t('User name is required')
        ],
        emailRules: [
          (v: string) => !!v || this.$t('User email is required'),
          (v: string) => /.+@.+\..+/.test(v) || this.$t('User email must be valid'),
          (v: string) => v.length <= 254 || this.$t('User email is too long'),
        ],
        nameRules: [
          (v: string) => !!v || this.$t('name.nameRequired'),
          (v: string) => /^[^\d]*$/.test(v) || this.$t('name.noNumbersAllowed')
        ],
        passwordRules: [
          (v: string) => !!v || this.$t('user.passwordRequired'),
          (v: string) => v.length >= 8 || this.$t('user.passwordTooShort')
        ]
      }
    },
    methods: {
      async create() {
        console.log('Método create chamado')
        if (!(this.$refs.form as Vue & { validate: () => boolean }).validate()) {
          return
        }
        this.loading = true
        this.errorMessage = ''
        try {
          await this.$repositories.user.create({
            first_name: this.firstName,
            last_name: this.lastName,
            username: this.username,
            email: this.email,
            first_name: this.first_name,
            last_name: this.last_name,
            password1: this.password1,
            password2: this.password2,
            is_superuser: this.isSuperuser,
            is_staff: this.isSuperuser ? true : this.isStaff
          })
          this.$emit('save')
        } catch (e: any) {
            console.error("Erro ao criar usuário:", e.response?.data || e.message)
            this.errorMessage = e.response?.data?.detail || JSON.stringify(e.response?.data) || this.$t('generic.error')
        }
 finally {
          this.loading = false
        }
      }
    }
  })
  </script>
  