<template>
    <v-app>
      <v-main>
        <v-container fluid class="fill-height">
          <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="6" class="text-center">
              <v-alert type="success" color="#1976D2" border="left" prominent>
                <h1 class="display-2 white--text">{{ message }}</h1>
                <p class="subtitle-1 white--text">
                  We will redirect you back to our homepage in {{ countdown }} seconds.
                </p>
              </v-alert>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    layout: 'custom-empty',
    data() {
      return {
        countdown: 3
      }
    },
    computed: {
      message() {
        return this.$route.query.message || 'Task successful!';
      }
    },
    mounted() {
      const timer = setInterval(() => {
        if (this.countdown > 1) {
          this.countdown--;
        } else {
          clearInterval(timer);
          this.$router.push({ path: '/' });
        }
      }, 1000);
    }
  }
  </script>
  
  <style scoped>
  .fill-height {
    min-height: 100vh;
  }
  </style>