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
          <text-classification />
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
import TextClassification from '~/components/containers/annotation/TextClassification'
import Paginator from '~/components/containers/annotation/Paginator'
import GuidelineButton from '@/components/containers/annotation/GuidelineButton'
import MetadataBox from '@/components/organisms/annotation/MetadataBox'
import BottomNavigator from '@/components/containers/annotation/BottomNavigator'

export default {
  layout: 'annotation',

  middleware: ['check-auth', 'auth'],

  components: {
    BottomNavigator,
    TextClassification,
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
