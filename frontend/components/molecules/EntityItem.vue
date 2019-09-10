<template>
  <span v-if="label" class="highlight bottom" :style="{ borderColor: color }">
    <span class="highlight__content">{{ content }}</span><span class="highlight__label" :data-label="label" :style="{backgroundColor: color}" @click="open" />
  </span>
  <span v-else>{{ content }}</span>
</template>

<script>
import { idealColor } from '~/plugins/utils.js'

export default {
  props: {
    content: {
      type: String,
      default: '',
      required: true
    },
    label: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: '#64FFDA'
    }
  },
  computed: {
    textColor() {
      return idealColor(this.color)
    }
  },
  methods: {
    open() {
      alert('hello')
    }
  }
}
</script>

<style scoped>
.highlight.blue {
    background: #edf4fa !important;
}
.highlight.bottom {
    display: block;
    white-space: normal;
}
.highlight:first-child {
    margin-left: 0;
}
.highlight {
    border: 2px solid;
    color: #232323;
    margin: 4px 6px 4px 3px;
    vertical-align: middle;
    box-shadow: 2px 4px 20px rgba(0,0,0,.1);
    position: relative;
    cursor: default;
    min-width: 26px;
    line-height: 22px;
    display: flex;
}
.highlight__content {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    padding: 2px 2px 0px 6px;
}
.highlight.bottom .highlight__content:after {
    content: " ";
    padding-right: 3px;
}
.highlight__label {
    line-height: 14px;
    padding-top: 1px;
    align-items: center;
    justify-content: center;
    display: flex;
    padding: 0 8px;
    text-align: center;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    color: white;
}
.highlight__label::after {
  content: attr(data-label);
}
</style>
