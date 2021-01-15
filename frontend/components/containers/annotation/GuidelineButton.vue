<template>
  <div style="display:inline;">
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          class="text-capitalize ps-1 pe-1"
          min-width="36"
          outlined
          v-on="on"
          @click="dialog=true"
        >
          <v-icon>
            mdi-book-open-outline
          </v-icon>
        </v-btn>
      </template>
      <span>Show guideline</span>
    </v-tooltip>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <guideline-card
        v-if="currentProject"
        :guideline-text="currentProject.guideline"
        @close="dialog=false"
      />
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import GuidelineCard from '@/components/organisms/annotation/GuidelineCard'

export default {
  components: {
    GuidelineCard
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapGetters('projects', ['currentProject'])
  }
}
</script>
