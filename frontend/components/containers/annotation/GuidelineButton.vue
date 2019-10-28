<template>
  <base-modal
    text="Show guideline"
  >
    <template v-if="currentProject" v-slot="slotProps">
      <guideline-card
        :guideline-text="currentProject.guideline"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import GuidelineCard from '@/components/organisms/annotation/GuidelineCard'

export default {
  components: {
    BaseModal,
    GuidelineCard
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
