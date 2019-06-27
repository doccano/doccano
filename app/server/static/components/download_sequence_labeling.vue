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
  pre.code-block(v-show="format == 'json'")
    code.json
      include ./examples/download_sequence_labeling.jsonl
      | ...

  pre.code-block(v-show="format == 'json1'")
    code.json
      include ./examples/download_sequence_labeling.json1l
      | ...

  pre.code-block(v-show="format == 'spacy'")
    code.spacy
      include ./examples/download_sequence_labeling.spacy.json
      | 
</template>

<script>
import uploadMixin from './uploadMixin';

export default uploadMixin;
</script>
