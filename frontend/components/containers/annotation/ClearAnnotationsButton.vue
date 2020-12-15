<template>
  <div>
    <v-btn
      :disabled="false"
      class="text-capitalize"
      outlined
      @click="handleClear()"
    >
      {{ "Clear Annotations" }}
    </v-btn>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  components: {

  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapState('documents', ['selected'])
  },

  methods: {
    ...mapActions('documents', ['clearAnnotations']),

    handleClear() {
      const projectId = this.$route.params.id
      this.clearAnnotations(projectId)
    }
  }
}
</script>
