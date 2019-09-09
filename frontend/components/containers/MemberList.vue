<template>
  <member-list
    :headers="headers"
    :members="items"
    :selected="selected"
    :loading="loading"
    @update-selected="updateSelected"
    @update-role="updateRole"
  />
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'
import MemberList from '@/components/organisms/MemberList'

export default {
  components: {
    MemberList
  },
  data() {
    return {
      headers: [
        {
          text: 'Name',
          align: 'left',
          sortable: false,
          value: 'username'
        },
        {
          text: 'Role',
          value: 'role'
        }
      ]
    }
  },

  computed: {
    ...mapState('members', ['items', 'selected', 'loading'])
  },

  created() {
    this.getMemberList()
  },

  methods: {
    ...mapActions('members', ['getMemberList', 'updateMemberRole']),
    ...mapMutations('members', ['updateSelected']),

    updateRole(payload) {
      const data = {
        projectId: this.$route.params.id,
        ...payload
      }
      this.updateMemberRole(data)
    }
  }
}
</script>
