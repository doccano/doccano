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

  label.radio
    input(
      type="radio"
      name="format"
      value="spacy"
      v-bind:checked="format == 'spacy'"
      v-model="format"
    )
    | SpaCy

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

  pre.code-block(v-show="format == 'spacy'")
    code.spacy
      include ./examples/upload_sequence_labeling.spacy.json
      | 
      
</template>

<script>
import { uploadMixin } from './mixin';

export default uploadMixin;
</script>
