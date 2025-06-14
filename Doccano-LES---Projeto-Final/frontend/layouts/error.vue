<template>
  <v-app dark>
    <v-container fill-height style="height: calc(100vh - 58px)">
      <v-layout align-center>
        <v-flex text-center>
          <h1 class="display-2 primary--text">Whoops, 404</h1>
          <p>The page you were looking for does not exist</p>
          <v-btn to="/" outlined color="primary"> Get me out of here! </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      pageNotFound: '404 Not Found',
      otherError: "The page you were looking for wasn't allowed to access."
    }
  },
  head() {
    const title = this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title
    }
  }
}
</script>
