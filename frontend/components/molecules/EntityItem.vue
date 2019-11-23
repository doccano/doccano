<template>
  <v-menu
    v-if="label"
    v-model="showMenu"
    offset-y
  >
    <template v-slot:activator="{ on }">
      <span class="highlight bottom" :style="{ borderColor: color }" v-on="on">
        <span class="highlight__content">{{ content }}<v-icon class="delete" @click.stop="remove">mdi-close-circle</v-icon></span><span class="highlight__label" :data-label="label" :style="{ backgroundColor: color, color: textColor }" />
      </span>
    </template>
    <v-list
      dense
      min-width="150"
      max-height="400"
      class="overflow-y-auto"
    >
      <v-list-item
        v-for="(item, i) in labels"
        :key="i"
        v-shortkey.once="[item.suffix_key]"
        @shortkey="update(item)"
        @click="update(item)"
      >
        <v-list-item-content>
          <v-list-item-title v-text="item.text" />
        </v-list-item-content>
        <v-list-item-action>
          <v-list-item-action-text v-text="item.suffix_key" />
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-menu>
  <span v-else>{{ content }}</span>
</template>

<script>
import Vue from 'vue'
import { idealColor } from '~/plugins/utils.js'
Vue.use(require('vue-shortkey'))

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
    },
    labels: {
      type: Array,
      default: () => [],
      required: true
    }
  },
  data() {
    return {
      showMenu: false
    }
  },
  computed: {
    textColor() {
      return idealColor(this.color)
    }
  },
  methods: {
    update(label) {
      this.$emit('update', label)
      this.showMenu = false
    },
    remove() {
      this.$emit('remove')
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
  margin: 4px 6px 4px 3px;
  vertical-align: middle;
  box-shadow: 2px 4px 20px rgba(0,0,0,.1);
  position: relative;
  cursor: default;
  min-width: 26px;
  line-height: 22px;
  display: flex;
}
.highlight .delete {
  top:-15px;
  left:-13px;
  position:absolute;
  display: none;
}
.highlight:hover .delete {
  display: block;
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
  display: block;
  font-size: 14px;
  -webkit-font-smoothing: subpixel-antialiased;
  letter-spacing: .1em;
}
</style>
