<template>
  <section>
    <v-parallax :src="require(`~/assets/vbanner.jpg`)" height="400" dark>
      <v-layout wrap align-center justify-center class="white--text">
        <v-flex text-right class="mr-5">
          <img src="~/assets/icon.png" alt="doccano" height="200" />
        </v-flex>
        <v-flex>
          <h1 class="mb-2 display-1 text-xs-center">
            {{ $t('home.mainTitle') }}
          </h1>
          <div class="mt-4">
            <v-btn large outlined color="white" href="https://github.com/doccano/doccano">
              <v-icon left>
                {{ mdiGithub }}
              </v-icon>
              GitHub
            </v-btn>
            <v-btn class="blue lighten-2 ml-5" dark large :href="localePath('/auth')">
              {{ $t('home.getStarted') }}
            </v-btn>
          </div>
        </v-flex>
      </v-layout>
    </v-parallax>
  </section>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiGithub } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      mdiGithub
    }
  }
})
</script>
