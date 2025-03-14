<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="pa-5" width="100%">
              <!-- Título centralizado -->
              <v-card-title class="text-h5 d-flex justify-center">Create User</v-card-title>
              <v-form v-model="valid" @submit.prevent="submitForm">
                <v-alert v-show="showError" v-model="showError" type="error" dismissible>
                  {{ errorMessage }}
                </v-alert>
                <v-text-field
                  v-model="name"
                  :rules="nameRules"
                  label="Name"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="email"
                  :rules="emailRules"
                  label="Email"
                  type="email"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  :rules="passwordRules"
                  label="Password"
                  type="password"
                  required
                ></v-text-field>
                <v-btn
                  type="submit"
                  color="primary"
                  block
                  :disabled="!valid"
                >
                  Register
                </v-btn>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      name: '',
      email: '',
      password: '',
      showError: false,
      errorMessage: '',
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
        (v) => (v && v.length >= 6) || 'Password must be at least 6 characters'
      ]
    }
  },
  methods: {
    submitForm() {
      if (!this.valid) {
        this.showError = true
        this.errorMessage = 'Please fill in all required fields correctly'
        return
      }
      console.log('Form submitted:', this.name, this.email, this.password)
      this.showError = false
    }
  }
}
</script>
