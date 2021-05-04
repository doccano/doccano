<template>
  <v-menu
      v-if="label"
      v-model="showMenu"
      offset-y
  >
    <template v-slot:activator="{ on }">
      <span :id="'spn-' + spanid" :style="{ borderColor: color }" class="highlight bottom" v-on="on">
        <span class="highlight__content">{{ content }}<v-icon class="delete" @click.stop="remove">mdi-close-circle</v-icon><span
            :class="{ active: spanid === selectedChunkId }" class="iconify target-selector" data-icon="mdi-link-variant"
            @click.stop="onLinkClick"></span></span><span :data-label="label" :style="{ backgroundColor: color, color: textColor }"
                                                          class="highlight__label"/>
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
          v-shortkey.once="[item.suffixKey]"
          @shortkey="update(item)"
          @click="update(item)"
      >
        <v-list-item-content>
          <v-list-item-title v-text="item.text"/>
        </v-list-item-content>
        <v-list-item-action>
          <v-list-item-action-text v-text="item.suffixKey"/>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-menu>
  <span v-else :class="[newline ? 'newline' : '']">{{ content }}</span>
</template>

<script>
import {idealColor} from '~/plugins/utils.js'

export default {
  props: {
    spanid: {
      type: Number,
      default: 0,
      required: true
    },
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
    },
    newline: {
      type: Boolean
    },
    selectedChunkId: {
      type: Number,
      default: -1
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
    },
    onLinkClick() {
      this.$emit('selectLinkSource');
      this.showMenu = false;
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
  box-shadow: 2px 4px 20px rgba(0, 0, 0, .1);
  position: relative;
  cursor: default;
  min-width: 26px;
  line-height: 22px;
  display: flex;
}

.highlight .delete {
  top: -15px;
  left: -13px;
  position: absolute;
  display: none;
}

.highlight:hover .delete {
  display: block;
}

.highlight .target-selector:before {
  content: 'L';
}

.highlight .target-selector {
  position: absolute;
  top: -12px;
  right: -11px;
  width: 20px;
  background: rgba(0, 0, 0, 0.54);
  color: #ffffff;
  border-radius: 30px;
  cursor: pointer;
  text-align: center;
}

.highlight .target-selector.active {
  display: block;
  background: #008ad6;
  color: #ffffff;
}

.highlight__content {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 2px 2px 0 6px;
  background: #ffffff;
}

.highlight.bottom .highlight__content:after {
  content: " ";
  padding-right: 3px;
}

.highlight__label {
  line-height: 14px;
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

.newline {
  width: 100%;
}
</style>
