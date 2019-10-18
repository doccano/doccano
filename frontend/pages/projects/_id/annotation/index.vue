<template>
  <v-content>
    <v-container fluid>
      <v-row
        no-gutters
        class="d-none d-sm-flex"
      >
        <v-col>
          <guideline-button />
        </v-col>
        <v-spacer />
        <v-col>
          <paginator />
        </v-col>
      </v-row>
      <bottom-navigator class="d-flex d-sm-none" />
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-card-text class="title">
              <entity-item-box />
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <metadata-box :metadata="JSON.parse(metadata)" />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import EntityItemBox from '~/components/containers/EntityItemBox'
import Paginator from '~/components/containers/Paginator'
import GuidelineButton from '@/components/containers/GuidelineButton'
import MetadataBox from '@/components/organisms/MetadataBox'
import BottomNavigator from '@/components/organisms/BottomNavigator'

export default {
  layout: 'annotation',

  components: {
    BottomNavigator,
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
