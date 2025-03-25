<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="pa-0 overflow-hidden rounded-lg" width="100%">
              <v-sheet color="primary" class="py-3 px-4 rounded-t">
                <div class="text-h6 font-weight-medium text--white">
                  Register User
                </div>
              </v-sheet>
              <v-card-text class="pa-6">
                <v-form v-model="valid" @submit.prevent="submitForm">
                  <v-alert
                    v-show="showError"
                    v-model="showError"
                    type="error"
                    dismissible
                    class="error-message"
                  >
                    {{ errorMessage }}
                  </v-alert>
                  
                  <v-text-field
                    v-model="name"
                    :rules="nameRules"
                    label="Username"
                    required
                    :prepend-icon="mdiAccount"
                  ></v-text-field>
                  
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="Email"
                    type="email"
                    required
                    :prepend-icon="mdiEmail"
                  ></v-text-field>

                  <v-text-field
                    v-model="password"
                    :rules="passwordRules"
                    label="Password"
                    type="password"
                    required
                    :prepend-icon="mdiLock"
                  ></v-text-field>

                  <v-text-field
                    v-model="confirmPassword"
                    :rules="confirmPasswordRules"
                    label="Confirm Password"
                    type="password"
                    required
                    :prepend-icon="mdiLockCheck"
                  ></v-text-field>

                  <v-select
                    v-model="role"
                    :items="roleOptions"
                    :rules="roleRules"
                    label="Role"
                    required
                    :prepend-icon="mdiAccountKey"
                    :color="selectedRoleColor"
                  ></v-select>
                  
                  <v-row justify="center" class="mt-5">
                    <v-col cols="12">
                      <v-btn type="submit" color="primary" block :disabled="!valid">
                        Register
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mdiAccount, mdiEmail, mdiLock, mdiLockCheck, mdiAccountKey } from '@mdi/js'

export default {
  data() {
    return {
      valid: false,
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: '',
      showError: false,
      errorMessage: '',
      mdiAccount,
      mdiEmail,
      mdiLock,
      mdiLockCheck,
      mdiAccountKey,
      commonPasswords: [
        'password',
        '12345678',
        'qwertyui',
        '12345678',
        'letmein!',
        'software',
        'password1'
      ],
      nameRules: [
        (v) => !!v || 'Name is required',
        (v) => (v && v.length >= 3) || 'Name must be at least 3 characters'
      ],
      emailRules: [
        (v) => !!v || 'Email is required',
        (v) => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ],
      passwordRules: [
        (v) => !!v || 'Password is required',
        (v) => (v && v.length >= 8) || 'Password must be at least 8 characters',
        (v) => (v && v.length <= 30) || 'Password must be less than 31 characters',
        (v) => !/^\d+$/.test(v) || 'Password cannot be entirely numerical',
        (v) => !this.commonPasswords.includes(v.toLowerCase()) || 'Password is too common',
        (v) => /[A-Z]/.test(v) || 'Password must contain at least one uppercase letter',
        (v) => /[a-z]/.test(v) || 'Password must contain at least one lowercase letter',
        (v) => /[0-9]/.test(v) || 'Password must include at least one digit',
        (v) => /[@$!%*?&#]/.test(v) || 'Password must include at least one special character'
      ],
      confirmPasswordRules: [
        (v) => !!v || 'Please confirm your password',
        (v) => v === this.password || 'Passwords do not match'
      ],
      roleRules: [
        (v) => !!v || 'Role is required'
      ],
      roleOptions: [
        { text: 'Annotator', value: 'annotator' },
        { text: 'Admin', value: 'admin' },
        { text: 'Owner', value: 'owner' }
      ]
    }
  },
  computed: {
    selectedRoleColor() {
      if (this.role === 'admin') {
        return '#FF2F00'
      } else if (this.role === 'owner') {
        return '#a8c400'
      } else {
        return 'primary'
      }
    }
  },
  watch: {
    password() {
      this.confirmPasswordRules = [
        (v) => !!v || 'Please confirm your password',
        (v) => v === this.password || 'Passwords do not match'
      ]
    }
  },
  methods: {
    async submitForm() {
      if (!this.valid) {
        this.showError = true;
        this.errorMessage = 'Please fill in all required fields correctly';
        return;
      }
      
      try {
        const userData = {
          username: this.name,
          email: this.email,
          password1: this.password,
          password2: this.password,
          role: this.role
        };
        const result = await this.$repositories.user.register(userData);
        console.log('User registered successfully:', result);
        this.showError = false;
        this.$router.push({
          path: '/message',
          query: { message: 'Registration Successful! 🦭' }
        });
      } catch (error) {
        this.showError = true;
        let errorDetail = '';
        if (error.response && error.response.data) {
          const errors = [];
          for (const [field, messages] of Object.entries(error.response.data)) {
            const fieldName = field.charAt(0).toUpperCase() + field.slice(1);
            const formattedMessages = Array.isArray(messages)
              ? messages.join(', ')
              : messages;
            errors.push(`${fieldName}: ${formattedMessages.replace(/^\n+/, '')}`);
          }
          errorDetail = errors.join('\n\n');
        } else {
          errorDetail = 'User registration failed';
        }
        this.errorMessage = errorDetail;
        console.error('Registration error:', error.response && error.response.data);
      }
    }
  }
}
</script>

<style scoped>
.error-message {
  white-space: pre-line;
}
</style>