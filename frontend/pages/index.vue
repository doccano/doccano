<template>
  <v-app>
    <div class="indexViewContainer">
      <div class="indexViewBackground"></div>

      <div class="indexViewContent">
        <img src="/doccana-logo.png" alt="Doccana Logo" class="indexViewLogo" draggable="false" />

        <h1 class="indexViewTitle display-1 text-xs-center">Welcome to doccana!</h1>

        <p class="indexViewSubtitle">Your go-to platform for document annotation and analysis..</p>

        <v-btn color="primary" large class="indexViewButton" @click="handleGetStartedClick">
          <strong>Start</strong>
        </v-btn>

        <div class="xs12 md4 indexViewCopyright">©2025 Doccana, Software Engineering Lab</div>
      </div>
    </div>
  </v-app>
</template>

<script>
export default {
  name: 'Index',
  layout: 'custom-empty',
  methods: {
    handleGetStartedClick() {
      this.$router.push('/home')
    }
  }
}
</script>

<style scoped>
.indexViewContainer {
  position: relative;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.indexViewBackground {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
}

.indexViewContent {
  position: relative;
  text-align: center;
  padding: 2rem;
  max-width: 700px;
  width: 100%;
  color: #000000;
}

.indexViewLogo {
  width: 600px;
  margin-bottom: 1rem;
}

.indexViewTitle {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
  color: #000000;
}

.indexViewSubtitle {
  font-size: 1.2rem;
  font-weight: 300;
  margin-bottom: 2rem;
  line-height: 1.6;
  opacity: 0.9;
  color: #333333;
}

.theme--dark .indexViewTitle {
  color: #ffffff;
}

.theme--dark .indexViewSubtitle {
  color: #cccccc;
}

.indexViewButton {
  font-size: 1rem;
  padding: 0.75rem 2rem;
  border-radius: 4px;
}

.indexViewCopyright {
  margin-top: 2rem;
  font-size: 0.9rem;
  font-weight: 300;
  color: #6c6c6c !important;
}
</style>