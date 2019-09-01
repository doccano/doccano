<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="mb-2 ml-2 text-capitalize"
        outlined
        :disabled="!isMemberSelected"
        @click="dialog=true"
      >
        Remove
      </v-btn>
    </template>
    <member-deletion-form
      :selected="selected"
      @remove="handleRemoveMember"
      @close="dialog=false"
    />
  </v-dialog>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import MemberDeletionForm from '@/components/organisms/MemberDeletionForm'

export default {
  components: {
    MemberDeletionForm
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    ...mapState('members', ['selected']),
    ...mapGetters('members', ['isMemberSelected'])
  },

  methods: {
    ...mapActions('members', ['removeMember']),

    handleRemoveMember() {
      const projectId = this.$route.params.id
      this.removeMember(projectId)
      this.dialog = false
    }
  }
}
</script>
