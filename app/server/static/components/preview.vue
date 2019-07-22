<template lang="pug">
div.preview
  object(v-if="isPDF", v-bind:data="url", type="application/pdf")
    embed(v-bind:src="url", type="application/pdf")
  iframe(v-else-if="isWord", v-bind:src="officeViewer")
  iframe(v-else, v-bind:src="url")
</template>

<style scoped>
.preview, object, iframe {
  width: 100%;
  height: 100%;
}
</style>

<script>
export default {
  props: {
    url: {
      type: String,
      default: '',
    },
  },

  computed: {
    fileExtension() {
      const filename = this.url.split('/').pop();
      const extension = filename.match(/[^#?]+/)[0].split('.').pop();
      return extension.toLowerCase();
    },

    isPDF() {
      return this.fileExtension === 'pdf';
    },

    isWord() {
      return [
        'doc',
        'dot',
        'docx',
        'docm',
        'dotm',
      ].indexOf(this.fileExtension) !== -1;
    },

    officeViewer() {
      return `https://view.officeapps.live.com/op/view.aspx?src=${encodeURIComponent(this.url)}`;
    },
  },
};
</script>
