<template>
  <div>
    <v-btn
      v-for="item in social"
      :key="item.provider"
      block
      elevation="2"
      color="secondary"
      :href="item.href"
      class="mt-5"
    >
      {{ $t('user.socialLogin', { provider: item.provider }) }}
    </v-btn>
  </div>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'

export default Vue.extend({
  props: {
    fetchSocialLink: {
      type: Function as PropType<() => Promise<any>>,
      required: true
    }
  },
  data() {
    return {
      social: {} as any
    }
  },
  async mounted() {
    try {
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
    } catch (e) {
      console.error(e)
    }
  }
})
</script>
