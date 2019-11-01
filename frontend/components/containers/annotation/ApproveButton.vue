<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        class="text-capitalize ps-1 pe-1"
        min-width="36"
        outlined
        v-on="on"
        @click="dialog=true"
      >
        <v-icon v-if="approved">
          mdi-checkbox-blank-circle-outline
        </v-icon>
        <v-icon v-else>
          mdi-check-circle-outline
        </v-icon>
      </v-btn>
    </template>
    <span>Approve</span>
  </v-tooltip>
</template>

<script>
export default {
  data() {
    return {
      approved: true
    }
  }
}
</script>
