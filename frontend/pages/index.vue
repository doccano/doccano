<template>
  <v-content>
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
    <v-container>
      <v-layout
        column
        wrap
        class="my-5"
        align-center
      >
        <v-flex xs12 sm4 class="my-3">
          <div class="text-xs-center">
            <h2 class="headline">
              The best features
            </h2>
          </div>
        </v-flex>
        <v-flex xs12>
          <v-container grid-list-xl>
            <v-layout wrap align-center>
              <v-flex xs12 md4>
                <v-card>
                  <v-img
                    src="/images/feature3.png"
                    height="200px"
                  />
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center font-weight-bold mb-2">
                      Team Collaboration
                    </div>
                  </v-card-title>
                  <v-card-text class="subtitle-1 layout justify-center">
                    Annotation with your team mates.
                  </v-card-text>
                </v-card>
              </v-flex>
              <v-flex xs12 md4>
                <v-card>
                  <v-img
                    src="/images/feature2.png"
                    height="200px"
                  />
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center font-weight-bold mb-2">
                      Any Language
                    </div>
                  </v-card-title>
                  <v-card-text class="subtitle-1 layout justify-center">
                    Annotation with any language.
                  </v-card-text>
                </v-card>
              </v-flex>
              <v-flex xs12 md4>
                <v-card>
                  <v-img
                    src="/images/feature1.png"
                    height="200px"
                  />
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center font-weight-bold mb-2">
                      Open Source
                    </div>
                  </v-card-title>
                  <v-card-text class="subtitle-1 layout justify-center">
                    Annotation with free and customizable.
                  </v-card-text>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </v-container>

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
  </v-content>
</template>

<script>
export default {
  components: {
  }
}
</script>
