<template>
  <div class="mt-10">
    <v-btn
      v-for="item in social"
      :key="item.provider"
      block
      elevation="2"
      color="secondary"
      :href="item.href"
    >
      Login With {{ item.provider }}
    </v-btn>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    fetchSocialLink: {
      type: Function,
      default: () => Promise
    }
  },
  data() {
    return {
      social: {}
    }
  },
  async mounted() {
    const response = await this.fetchSocialLink()
    this.social = Object.entries(response)
      .map(([key, value]: any) => ({
        provider: key,
        value
      }))
      .filter((item) => !!item.value?.authorize_url)
      .map((item: any) => ({
        ...item,
        href: `${item.value.authorize_url}&redirect_uri=${location.origin}${item.value.redirect_path}`
      }))
  }
})
</script>
