<template lang="pug">
extends ./download.pug

block select-format-area
  label.radio
    input(
      type="radio"
      name="format"
      value="json"
      v-bind:checked="format == 'json'"
      v-model="format"
    )
    | JSONL

  label.radio
    input(
      type="radio"
      name="format"
      value="json1"
      v-bind:checked="format == 'json1'"
      v-model="format"
    )
    | JSON(Text-Labels)

block example-format-area
  pre.code-block(v-show="format == 'json'")
    code.json
      include ./examples/download_sequence_labeling.jsonl
      | ...

  pre.code-block(v-show="format == 'json1'")
    code.json
      include ./examples/download_sequence_labeling.json1l
      | ...
</template>

<script>
import uploadMixin from './uploadMixin';

export default uploadMixin;
</script>
