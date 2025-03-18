<template>
  <v-app id="inspire">
      <v-main>
          <v-container class="fill-height" fluid>
              <!-- New section to display all users -->
              <v-row align="center" justify="center" class="mt-5">
                  <v-col cols="12" sm="8" md="6">
                      <v-card class="pa-0 overflow-hidden rounded-lg" width="100%">
                          <v-sheet color="primary" class="py-3 px-4 rounded-t">
                              <div class="text-h6 font-weight-medium text-black">
                                  All Users
                              </div>
                          </v-sheet>
                          <v-card-text class="pa-6">
                              <v-list>
                                  <v-list-item-group>
                                      <v-list-item v-for="user in sortedUsers" :key="user.id">
                                          <v-list-item-content>
                                            <v-list-item-title>
                                              {{ user.username }}
                                            </v-list-item-title>
                                              <v-list-item-subtitle>
                                                  {{ user.email }}
                                              </v-list-item-subtitle>
                                          </v-list-item-content>
                                      </v-list-item>
                                  </v-list-item-group>
                              </v-list>
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
      confirmPassword: '',
      role: 'annotator',
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
        (v) =>
          (v && v.length >= 8) ||
          'Password must be at least 8 characters',
        (v) =>
          (v && v.length <= 30) ||
          'Password must be less than 31 characters'
      ],
      confirmPasswordRules: [
        (v) => !!v || 'Please confirm your password',
        (v) => v === this.password || 'Passwords do not match'
      ],
      roleOptions: [
        { text: 'Admin', value: 'admin' },
        { text: 'Annotator', value: 'annotator' }
      ],
      users: []  // <-- add users array for listing users
    }
  },
  computed: {
    sortedUsers() {
      return [...this.users].sort((a, b) => a.id - b.id)
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
  created() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
            const response = await this.$axios.get('/v1/users/')
            console.log('Fetched users:', response.data);
            this.users = response.data
        } catch (error) {
            console.error('Error fetching users:', error)
        }
    },
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
      } catch (error) {
        this.showError = true;
        let errorDetail = '';
        if (error.response && error.response.data) {
          for (const [field, messages] of Object.entries(error.response.data)) {
            if (Array.isArray(messages)) {
              errorDetail += `<strong>${field}:</strong> ${messages.join(', ')}<br/>`;
            } else {
              errorDetail += `<strong>${field}:</strong> ${messages}<br/>`;
            }
          }
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