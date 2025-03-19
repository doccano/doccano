<template>
    <div class="admin-container">
      <div class="delete-user-box">
        <h2>Delete User</h2>
        <v-text-field
          v-model="username"
          label="Enter Username"
          outlined
          dense
        />
        <v-btn color="red" @click="deleteUser">
          Delete
        </v-btn>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { APIUserRepository } from '~/repositories/user/apiUserRepository'
  
  export default Vue.extend({
    name: 'Admin',
    data() {
      return {
        username: "" // Stores the username input
      }
    },
    methods: {
      async deleteUser() {
        if (!this.username) {
          alert("Please enter a username.");
          return;
        }
  
        try {
          const userRepository = new APIUserRepository();
          // Retrieve the user id by username using the repository
          const userId = await userRepository.getIdByUsername(this.username);
          if (!userId) {
            alert("User not found.");
            return;
          }
  
          // Prevent self-deletion: check if the user id matches the logged in user's id
          if (userId === this.$store.state.auth.id) {
            alert("You cannot delete yourself.");
            return;
          }
  
          // Delete the user using the repository method
          await userRepository.delete(userId);
          alert("User deleted successfully.");
          this.username = "";
        } catch (error: any) {
          console.error("Error deleting user:", error);
          alert("An error occurred. Please try again.");
        }
      }
    }
  });
  </script>
  
  <style scoped>
  .admin-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    flex-direction: column;
  }
  
  .delete-user-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  </style>