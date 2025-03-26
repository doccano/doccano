<template>
  <v-app>
    <v-main>
      <v-container fluid class="fill-height">
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="6" class="text-center">
            <transition name="fade">
              <v-alert
                v-if="showAlert"
                key="alert"
                type="success"
                color="primary"
                border="left"
                prominent
              >
                <div>
                  <span class="base-message">{{ baseMessage }}</span
                  ><br />
                  <span class="redirect-message">{{ redirectText }}</span>
                </div>
              </v-alert>
            </transition>
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
      countdown: 3,
      showAlert: true
    }
  },
  computed: {
    baseMessage() {
      return this.$route.query.message || 'Task successful!'
    },
    redirectText() {
      const redirectPath = this.$route.query.redirect || '/home'
      if (redirectPath === '/home') {
        return ` You will be redirected to our homepage in ${this.countdown} seconds.`
      } else if (redirectPath === '/edit-user') {
        return ` You will be redirected to the edit user list in ${this.countdown} seconds.`
      } else {
        return ` You will be redirected in ${this.countdown} seconds.`
      }
    }
  },
  mounted() {
    const redirectPath = this.$route.query.redirect || '/home'
    const timer = setInterval(() => {
      if (this.countdown > 1) {
        this.countdown--
      } else {
        clearInterval(timer)
        this.showAlert = false
        setTimeout(() => {
          this.$router.push({ path: redirectPath })
        }, 500)
      }
    }, 1000)
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.base-message {
  font-size: 2.5rem;
}

.redirect-message {
  font-size: 1.5rem;
}

.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-leave-to {
  opacity: 0;
}
</style>
