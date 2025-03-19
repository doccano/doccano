<template>
    <v-text-field
      v-model="email"
      label="Email"
      type="email"
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
      email: {
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
  