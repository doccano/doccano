<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <login-form
              :login="authenticateUser"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapActions } from 'vuex'
import LoginForm from '@/components/organisms/auth/LoginForm'

export default {
  components: {
    LoginForm
  },

  methods: {
    ...mapActions('auth', ['authenticateUser'])
  }
}
</script>
