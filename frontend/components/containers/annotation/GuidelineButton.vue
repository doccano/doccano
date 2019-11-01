<template>
  <div>
    <v-btn
      class="text-capitalize"
      outlined
      @click="dialog=true"
    >
      Show guideline
    </v-btn>
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
