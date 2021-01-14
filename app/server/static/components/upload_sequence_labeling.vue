<template lang="pug">
extends ./upload.pug

block select-format-area
  label.radio
    input(
      type="radio"
      name="format"
      value="conll"
      v-bind:checked="format == 'conll'"
      v-model="format"
    )
    | CoNLL

  label.radio
    input(
      type="radio"
      name="format"
      value="json"
      v-bind:checked="format == 'json'"
      v-model="format"
    )
    | JSONL

block example-format-area
  pre.code-block(v-show="format == 'plain'")
    code.plaintext
      include ./examples/upload_sequence_labeling.txt
      | ...

  pre.code-block(v-show="format == 'conll'")
    code.plaintext
      include ./examples/upload_sequence_labeling.conll
      | ...

  pre.code-block(v-show="format == 'json'")
    code.json
      include ./examples/upload_sequence_labeling.jsonl
      | ...
</template>

<script>
import uploadMixin from './uploadMixin';

export default uploadMixin;
</script>
