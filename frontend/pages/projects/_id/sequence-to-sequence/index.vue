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
      <v-row justify="center">
        <v-col cols="12" md="9">
          <seq2seq-container />
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
import Seq2seqContainer from '~/components/containers/annotation/Seq2seqContainer'
import Paginator from '~/components/containers/annotation/Paginator'
import GuidelineButton from '@/components/containers/annotation/GuidelineButton'
import MetadataBox from '@/components/organisms/annotation/MetadataBox'

export default {
  layout: 'annotation',

  middleware: ['check-auth', 'auth'],

  components: {
    Seq2seqContainer,
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
