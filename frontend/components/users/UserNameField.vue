<template>
    <v-text-field
      v-model="username"
      label="Username"
      outlined
      required
    />
  </template>
  
  <script lang="ts">
  import Vue from "vue";
  
  export default Vue.extend({
    props: {
      value: {
        type: String,
        required: true,
      },
    },
    computed: {
      username: {
        get(): string {
          return this.value;
        },
        set(newValue: string): void {
          this.$emit("input", newValue);
        },
      },
    },
  });
  </script>
  