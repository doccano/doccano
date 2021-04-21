<template lang="pug">
extends ./annotation.pug

block annotation-area
  div.card.has-text-weight-bold.has-text-white.has-background-royalblue
    div.card-content
      div.content
        audio(
          ref="player"
          controls
          v-bind:src="audioFile"
          v-shortkey="{ playOrPauseAudio: ['alt', 'p'] }"
          v-on:shortkey="playOrPauseAudio"
        )

  section
    header.header
      textarea.textarea(
        v-model="transcription"
        v-debounce="syncTranscription"
        type="text"
        placeholder="Transcribe audio here..."
        autofocus
      )
</template>

<style scoped>
audio {
  height: 3em;
  width: 100%;
  display: block;
  margin: 0 auto;
}
</style>

<script>
import annotationMixin from './annotationMixin';
import HTTP from './http';

export default {
  mixins: [annotationMixin],

  data: () => ({
    transcription: '',
    isAudioPlaying: false,
  }),

  computed: {
    annotation() {
      const annotations = this.annotations[this.pageNumber];
      return annotations && annotations[0];
    },

    audioFile() {
      const docs = this.docs[this.pageNumber];
      return docs && docs.text;
    },
  },

  watch: {
    annotations() {
      this.updateTranscription();
    },

    pageNumber() {
      this.updateTranscription();
    },
  },

  methods: {
    async playOrPauseAudio() {
      const player = this.$refs.player;
      if (this.isAudioPlaying) {
        player.pause();
        this.isAudioPlaying = false;
      } else {
        await player.play();
        this.isAudioPlaying = true;
      }
    },

    updateTranscription() {
      const text = this.annotation && this.annotation.text;
      this.transcription = text || '';
    },

    async syncTranscription(text) {
      const docId = this.docs[this.pageNumber].id;
      const annotations = this.annotations[this.pageNumber];
      const hasTranscription = text.trim().length > 0;

      if (!hasTranscription && !this.annotation) {
        return;
      }

      if (!hasTranscription && this.annotation) {
        await HTTP.delete(`docs/${docId}/annotations/${this.annotation.id}`);
        annotations.splice(0, annotations.length);
        return;
      }

      if (this.annotation) {
        const annotation = { ...this.annotation, text };
        await HTTP.put(`docs/${docId}/annotations/${this.annotation.id}`, annotation);
      } else {
        const annotation = { text };
        const response = await HTTP.post(`docs/${docId}/annotations`, annotation);
        annotations.unshift({ ...response.data, text });
      }
    },

    async submit() {
      const state = this.getState();
      this.url = `docs?q=${this.searchQuery}&speech2text_annotations__isnull=${state}&offset=${this.offset}&ordering=${this.ordering}`;
      await this.search();
      this.pageNumber = 0;
    },
  },
};
</script>
