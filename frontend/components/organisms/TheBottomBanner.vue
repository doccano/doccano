<template>
  <section>
    <v-parallax
      src="/images/vbanner.jpg"
      height="400"
      dark
    >
      <v-container>
        <v-layout
          wrap
          align-center
          justify-center
          class="white--text"
        >
          <v-flex
            xs12
            md7
          >
            <v-img
              src="http://doccano.herokuapp.com/static/images/named_entity_recognition.6fb82064e7aa.png"
              max-height="380"
              contain
              class="ma-5"
            />
          </v-flex>
          <v-flex
            xs12
            md5
          >
            <h1 class="mb-2 display-1 text-xs-center">
              Realize your ideas quickly
            </h1>
            <div class="mt-4">
              <v-btn
                class="blue lighten-2"
                dark
                large
                href="/demo"
              >
                Try demo
              </v-btn>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-parallax>
  </section>
</template>
