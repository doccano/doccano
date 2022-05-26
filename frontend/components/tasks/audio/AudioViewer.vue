<template>
  <div>
    <div id="waveform" />
    <v-row no-gutters align="center" class="mb-3 mt-1">
      <v-col md="8">
        <v-slider
          v-model="zoom"
          min="0"
          max="500"
          step="10"
          :append-icon="mdiMagnifyPlusOutline"
          :prepend-icon="mdiMagnifyMinusOutline"
          hide-details
          @click:append="zoomIn"
          @click:prepend="zoomOut"
          @change="onChangeZoom"
        />
      </v-col>
      <v-col md="2">
        <v-slider
          v-model="volume"
          min="0"
          max="1"
          step="0.1"
          :append-icon="mdiVolumeHigh"
          hide-details
          @change="onChangeVolume"
        />
      </v-col>
      <v-col md="2">
        <v-select
          v-model="speed"
          :items="speeds"
          label="Speed"
          dense
          outlined
          hide-details
          @change="onChangeSpeed"
        />
      </v-col>
    </v-row>
    <v-btn color="primary" class="text-capitalize" @click="play">
      <v-icon v-if="!isPlaying" left>
        {{ mdiPlayCircleOutline }}
      </v-icon>
      <v-icon v-else left>
        {{ mdiPauseCircleOutline }}
      </v-icon>
      <span v-if="!isPlaying">Play</span>
      <span v-else>Pause</span>
    </v-btn>
  </div>
</template>

<script>
import Vue from 'vue'
import WaveSurfer from 'wavesurfer.js'
import {
  mdiPlayCircleOutline,
  mdiPauseCircleOutline,
  mdiVolumeHigh,
  mdiMagnifyPlusOutline,
  mdiMagnifyMinusOutline
} from '@mdi/js'

export default Vue.extend({
  props: {
    source: {
      type: String,
      default: '',
      required: true
    }
  },

  data() {
    return {
      wavesurfer: null,
      isPlaying: false,
      zoom: 0,
      volume: 0.6,
      speed: 1,
      speeds: [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
      mdiPlayCircleOutline,
      mdiPauseCircleOutline,
      mdiVolumeHigh,
      mdiMagnifyPlusOutline,
      mdiMagnifyMinusOutline
    }
  },

  watch: {
    source() {
      this.load()
      this.isPlaying = false
    }
  },

  mounted() {
    this.wavesurfer = WaveSurfer.create({
      container: '#waveform',
      backend: 'MediaElement'
    })
    this.load()
  },

  methods: {
    load() {
      this.wavesurfer.load(this.source)
    },
    play() {
      this.isPlaying = !this.isPlaying
      this.wavesurfer.playPause()
    },
    zoomOut() {
      this.zoom = this.zoom - 10 || 0
      this.onChangeZoom(this.zoom)
    },
    zoomIn() {
      this.zoom = this.zoom + 10 || 500
      this.onChangeZoom(this.zoom)
    },
    onChangeVolume(value) {
      this.wavesurfer.setVolume(value)
    },
    onChangeZoom(value) {
      this.wavesurfer.zoom(value)
    },
    onChangeSpeed(value) {
      this.wavesurfer.setPlaybackRate(value)
    }
  }
})
</script>
