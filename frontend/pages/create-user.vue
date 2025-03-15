<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="pa-0 overflow-hidden rounded-lg" width="100%">
        
              <v-sheet color="primary" class="py-3 px-4 rounded-t">
                <div class="text-h6 font-weight-medium text-black">
                  Create User
                </div>
              </v-sheet>

              <v-card-text class="pa-6">
                <v-form v-model="valid" @submit.prevent="submitForm">
                  <v-alert v-show="showError" v-model="showError" type="error" dismissible>
                    {{ errorMessage }}
                  </v-alert>
                  
                  <v-text-field
                    v-model="name"
                    :rules="nameRules"
                    label="Username"
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
                  
                  <v-row justify="center" class="mt-5">
                    <v-col cols="12">
                      <v-btn
                        type="submit"
                        color="primary"
                        block
                        :disabled="!valid"
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
