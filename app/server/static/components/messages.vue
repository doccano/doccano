<template lang="pug">
  div(v-if="messages.length > 0")
    article.message.is-danger
      div.message-body
        ul
          li(v-for="message in messages", v-bind:key="message") {{ message }}
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
