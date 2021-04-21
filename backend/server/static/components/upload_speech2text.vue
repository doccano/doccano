<template lang="pug">
extends ./upload.pug

block select-format-area
  label.radio
    input(
      type="radio"
      name="format"
      value="json"
      v-bind:checked="format === 'json'"
      v-model="format"
    )
    | JSONL

  label.radio
    input(
      type="radio"
      name="format"
      value="audio"
      v-bind:checked="format === 'audio'"
      v-model="format"
    )
    | Audio

block example-format-area
  pre.code-block(v-show="format === 'json'")
    code.json
      include ./examples/upload_speech2text.jsonl
      | ...
</template>

<script>
import uploadMixin from './uploadMixin';

export default uploadMixin;
</script>
