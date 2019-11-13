<template>
  <base-modal
    text="Add"
    :is-create="true"
  >
    <template v-slot="slotProps">
      <member-addition-form
        :add-member="addMember"
        :items="items"
        :roles="roles"
        @close="slotProps.close"
        @search-user="searchUser"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import MemberAdditionForm from '@/components/organisms/members/MemberAdditionForm'
import UserService from '@/services/user.service'

export default {
  components: {
    BaseModal,
    MemberAdditionForm
  },

  data() {
    return {
      items: []
    }
  },

  computed: {
    ...mapGetters('roles', ['roles'])
  },

  created() {
    this.getRoleList()
  },

  methods: {
    ...mapActions('members', ['addMember']),
    ...mapActions('roles', ['getRoleList']),

    searchUser(username) {
      UserService.getUserList(username)
        .then((response) => {
          this.items = response.data
        })
        .catch((error) => {
          alert(error)
        })
    }
  }
}
</script>
