<template>
  <v-content>
    <v-container fluid>
      <v-row
        no-gutters
        class="d-none d-sm-flex"
      >
        <v-col v-if="currentDoc">
          <approve-button :approved="approved" />
          <filter-button />
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
import FilterButton from '@/components/containers/annotation/FilterButton'
import ApproveButton from '@/components/containers/annotation/ApproveButton'

export default {
  layout: 'annotation',

  middleware: ['check-auth', 'auth'],

  components: {
    ApproveButton,
    FilterButton,
    Seq2seqContainer,
    Paginator,
    GuidelineButton,
    MetadataBox
  },

  computed: {
    ...mapGetters('documents', ['currentDoc', 'approved'])
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
