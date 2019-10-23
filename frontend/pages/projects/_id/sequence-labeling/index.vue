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
          <metadata-box
            v-if="currentDoc"
            :metadata="JSON.parse(currentDoc.meta)"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
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

  computed: {
    ...mapGetters('documents', ['currentDoc'])
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
