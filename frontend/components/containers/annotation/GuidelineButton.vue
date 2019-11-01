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
    <base-dialog :dialog="dialog">
      <guideline-card
        v-if="currentProject"
        :guideline-text="currentProject.guideline"
        @close="dialog=false"
      />
    </base-dialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import BaseDialog from '@/components/molecules/BaseDialog'
import GuidelineCard from '@/components/organisms/annotation/GuidelineCard'

export default {
  components: {
    BaseDialog,
    GuidelineCard
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapGetters('projects', ['currentProject'])
  },

  created() {
    this.setCurrentProject(this.$route.params.id)
  },

  methods: {
    ...mapActions('projects', ['setCurrentProject'])
  }
}
</script>
