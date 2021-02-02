<template>
  <confirm-dialog
    :disabled="!isCommentSelected"
    :items="selectedComments"
    :title="$t('comments.removeComment')"
    :message="$t('comments.removePrompt')"
    :button-true-text="$t('generic.yes')"
    :button-false-text="$t('generic.cancel')"
    item-key="text"
    @ok="handleRemoveComment()"
  />
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import ConfirmDialog from '@/components/organisms/utils/ConfirmDialog'

export default {
  components: {
    ConfirmDialog
  },

  computed: {
    ...mapState('comments', ['selectedComments']),
    ...mapGetters('comments', ['isCommentSelected'])
  },

  methods: {
    ...mapActions('comments', ['deleteComment']),

    handleRemoveComment() {
      this.deleteComment({
        projectId: this.$route.params.id
      })
    }
  }
}
</script>
