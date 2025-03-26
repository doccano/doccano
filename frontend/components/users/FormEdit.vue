<template>
    <v-card>
      <v-card-title>{{ $t('generic.edit') }}</v-card-title>
      <v-card-text>
        <v-form v-model="valid" ref="form">
          <v-text-field v-model="first_name" :label="$t('First Name')" :rules="firstNameRules" required />
          <v-text-field v-model="last_name" :label="$t('Last Name')" :rules="lastNameRules" required />
          <v-text-field v-model="username" :label="$t('Username')" :rules="usernameRules" required />
          <v-text-field v-model="email" :label="$t('Email')" :rules="emailRules" type="email" required />
  
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
          {{ $t('update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { User } from '~/domain/models/user'
  
  export default Vue.extend({
    props: {
      user: {
        type: Object as () => User,
        required: true
      }
    },
    data() {
      return {
        valid: false,
        loading: false,
        first_name: '',
        last_name: '',
        username: '',
        email: '',
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
        ]
      }
    },
    watch: {
      user: {
        handler(user) {
          if (user) {
            this.first_name = user.first_name || ''
            this.last_name = user.last_name || ''
            this.username = user.username || ''
            this.email = user.email || ''
            this.isSuperuser = user.isSuperuser || false
            this.isStaff = user.isStaff || false
          }
        },
        immediate: true
      }
    },
    methods: {
      async saveUser() {
        if (!(this.$refs.form as Vue & { validate: () => boolean }).validate()) {
          return
        }
  
        this.loading = true
        this.errorMessage = ''
  
        try {
          const updatedUser = {
            ...this.user,
            first_name: this.first_name,
            last_name: this.last_name,
            username: this.username,
            email: this.email,
            isSuperuser: this.isSuperuser,
            isStaff: this.isStaff
          }
  
          await this.$emit('save', updatedUser)
        } catch (e: any) {
          this.errorMessage = e.response?.data?.detail || this.$t('generic.error')
        } finally {
          this.loading = false
        }
      }
    }
  })
  </script>  