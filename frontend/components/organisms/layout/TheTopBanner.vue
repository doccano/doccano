<template>
  <section>
    <v-parallax
      src="/images/vbanner.jpg"
      height="400"
      dark
    >
      <v-layout
        wrap
        align-center
        justify-center
        class="white--text"
      >
        <v-flex text-right class="mr-5">
          <img src="~/assets/icon.png" alt="doccano" height="200">
        </v-flex>
        <v-flex>
          <h1 class="mb-2 display-1 text-xs-center">
            Text Annotation for Human
          </h1>
          <div class="mt-4">
            <v-btn
              large
              outlined
              color="white"
              href="https://github.com/chakki-works/doccano"
            >
              <v-icon left>
                mdi-github-circle
              </v-icon>
              GitHub
            </v-btn>
            <v-btn
              class="blue lighten-2 ml-5"
              dark
              large
              href="/auth"
            >
              Get Started
            </v-btn>
          </div>
        </v-flex>
      </v-layout>
    </v-parallax>
  </section>
</template>
