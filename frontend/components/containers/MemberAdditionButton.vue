<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="mb-2 text-capitalize"
        color="primary"
        @click="dialog=true"
      >
        Add Member
      </v-btn>
    </template>
    <member-addition-form
      :add-member="addMember"
      :items="items"
      @close="dialog=false"
      @search-user="searchUser"
    />
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex'
import MemberAdditionForm from '@/components/organisms/MemberAdditionForm'
import UserService from '@/services/user.service'

export default {
  components: {
    MemberAdditionForm
  },

  data() {
    return {
      dialog: false,
      items: []
    }
  },

  methods: {
    ...mapActions('members', ['addMember']),

    searchUser(username) {
      UserService.getUserList(username)
        .then((response) => {
          this.items = response
        })
        .catch((error) => {
          alert(error)
        })
    }
  }
}
</script>
