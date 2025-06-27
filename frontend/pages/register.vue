<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <form-register :register="registerUser" />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapActions } from 'vuex'
import FormRegister from '@/components/auth/FormRegister.vue'

export default Vue.extend({
  components: {
    FormRegister,
  },

  methods: {
    ...mapActions('auth', ['registerUser'])
  }
})
</script>