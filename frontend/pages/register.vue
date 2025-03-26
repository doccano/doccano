<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="pa-0 overflow-hidden rounded-lg" width="100%">
              <v-sheet color="primary" class="py-3 px-4 rounded-t">
                <div class="text-h6 font-weight-medium" style="color: white">Register User</div>
              </v-sheet>
              <v-card-text class="pa-6">
                <v-form ref="registerForm" v-model="valid" @submit.prevent="submitForm">
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

                  <v-row justify="end" class="mt-5">
                    <v-col cols="auto" class="pr-custom">
                      <v-btn
                        :disabled="!valid"
                        class="text-none"
                        text
                        data-test="register-button"
                        @click="submitForm"
                      >
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
        'password1',
        'iloveyou',
        'sunshine',
        'football',
        'princess',
        'friend123',
        'welcome1',
        'charlie1',
        'superman',
        'baseball',
        'dragon12',
        'trustno1',
        'freedom1',
        'whatever',
        'computer',
        'michelle',
        'jessica1',
        'tiger123',
        'password123',
        'abc12345',
        '123456789',
        'sunflower',
        'lovely12',
        'secret77',
        'admin123',
        'qazwsxedc',
        'passw0rd',
        'starwars',
        'master123',
        'hello123',
        'football1',
        'qwerty123',
        '1234567890',
        '1q2w3e4r',
        '87654321',
        'loveyou1',
        'password!',
        'test1234',
        'flower123',
        'mustang1',
        'shadow12',
        'sunshine1'
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
      roleRules: [(v) => !!v || 'Role is required'],
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
        this.showError = true
        this.errorMessage = 'Please fill in all required fields correctly'
        return
      }

      try {
        const userData = {
          username: this.name,
          email: this.email,
          password1: this.password,
          password2: this.password,
          role: this.role
        }
        const result = await this.$repositories.user.register(userData)
        console.log('User registered successfully:', result)
        this.showError = false
        this.$router.push({
          path: '/message',
          query: { message: 'Register Successful! 🦭' }
        })
      } catch (error) {
        this.showError = true
        let errorDetail = ''
        if (error.response && error.response.data) {
          const data = error.response.data
          if (data.username) {
            errorDetail = "Error: A user with this username already exists in our database!"
          } else if (data.email) {
            errorDetail = "Error: A user with this email already exists in our database!"
          } else if (typeof data === 'string' && data.trim().startsWith('<')) {
            errorDetail = "Error: Can't access our database!"
          } else {
            const errors = []
            for (const [field, messages] of Object.entries(data)) {
              const formattedMessages =
                Array.isArray(messages) ? messages.join(', ') : messages
              errors.push(
                `${field.charAt(0).toUpperCase() + field.slice(1)}: ${formattedMessages.replace(/^\n+/, '').trim()}`
              )
            }
            errorDetail = errors.join('\n\n').trim()
          }
        } else {
          errorDetail = 'An error occurred'
        }
        this.errorMessage = errorDetail

        this.name = ''
        this.email = ''
        this.password = ''
        this.confirmPassword = ''
        this.role = ''

        if (this.$refs.registerForm) {
          this.$refs.registerForm.resetValidation()
        }

        console.error('Registration error:', error.response && error.response.data)
      }
    }
  }
}
</script>

<style scoped>
.error-message {
  white-space: normal;
}

.pr-custom {
  padding-bottom: -400px;
  padding-right: -3000px;
}
</style>
