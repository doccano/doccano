<template lang="pug">
extends ./annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue
        div.field.is-grouped.is-grouped-multiline
          div.control
            div.tags.has-addons
              a.tag.is-medium
    div.card-content
      div.content
        p Here comes the text - to be developped
</template>

<style scoped>
.card-header-title {
  padding: 1.5rem;
}
</style>
