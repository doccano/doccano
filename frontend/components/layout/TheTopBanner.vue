<template>
  <section>
    <v-parallax :src="require(`~/assets/vbanner.jpg`)" height="400" dark>
      <v-layout wrap align-center justify-center class="black--text">
        <v-flex text-right class="mr-5">
          <img src="~/assets/icon.png" alt="doccana" height="200" draggable="false" />
        </v-flex>
        <v-flex>
          <h1 class="mb-2 display-1 text-xs-center">
            {{ $t('home.mainTitle') }}
          </h1>
          <div class="mt-4">
            <v-btn
              large
              outlined
              color="black"
              href="https://github.com/GONCALOUNI/Software-Engineering-Lab"
            >
              <v-icon left>
                {{ mdiGithub }}
              </v-icon>
              GitHub
            </v-btn>
            <v-btn class="black lighten-2 ml-5" dark large :href="localePath('/register')">
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
