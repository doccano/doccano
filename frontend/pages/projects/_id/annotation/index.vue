<template>
  <v-content>
    <v-container fluid grid-list-md>
      <v-layout justify-center row wrap>
        <!--
        <v-flex d-flex xs12 sm12 md12>
          <v-card color="transparent elevation-0">
            <v-card-title>
              <guideline-button />
              <v-spacer />
              <paginator />
            </v-card-title>
          </v-card>
        </v-flex>
        -->
        <v-flex d-flex xs12 sm6 md9>
          <v-card width="100%">
            <v-card-title>
              <guideline-button />
              <v-spacer />
              <paginator />
            </v-card-title>
            <v-card-text class="title">
              <entity-item-box />
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex d-flex xs12 sm6 md3>
          <metadata-box :metadata="JSON.parse(metadata)" style="width:100%" />
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import EntityItemBox from '~/components/containers/EntityItemBox'
import Paginator from '~/components/containers/Paginator'
import GuidelineButton from '@/components/containers/GuidelineButton'
import MetadataBox from '@/components/organisms/MetadataBox'

export default {
  layout: 'annotation',

  components: {
    EntityItemBox,
    Paginator,
    GuidelineButton,
    MetadataBox
  },

  data() {
    return {
      metadata: '{"wikiPageId":2}'
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
