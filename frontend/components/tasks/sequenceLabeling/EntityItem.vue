<template>
  <v-menu
      v-if="label && !activeMenu"
      v-model="showMenu"
      offset-y
  >
    <template #activator="{ on }">
      <span :id="'spn-' + spanid" :style="{ borderColor: color }" class="highlight bottom" v-on="on">
        <span class="highlight__content">{{ content }}<v-icon class="delete" @click.stop="remove">mdi-close-circle</v-icon><span
            v-if="!showMenu && sourceChunk.none" class="choose-link-type" @click.stop="showActiveLinks"></span><span
            v-if="!showMenu && sourceChunk.id === spanid" class="active-link-source" @click.stop="abortNewLink"></span><span
            v-if="sourceLinkType.id > -1 && sourceChunk.id && sourceChunk.id !== spanid" class="choose-target"
            @click.stop="selectTarget"></span></span><span
          :data-label="label" :style="{ backgroundColor: color, color: textColor }" class="highlight__label"/>
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

  <v-menu
      v-else-if="label && activeMenu==='active-links'"
      v-model="showActiveLinksMenu"
      offset-y
  >
    <template #activator="{ on }">
      <span :id="'spn-' + spanid" :style="{ borderColor: color }" class="highlight bottom" v-on="on">
        <span class="highlight__content">{{ content }}<v-icon class="delete" @click.stop="remove">mdi-close-circle</v-icon><span
            class="active-link-source" @click.stop="abortNewLink"></span></span><span
          :data-label="label" :style="{ backgroundColor: color, color: textColor }" class="highlight__label"/>
      </span>
    </template>

    <v-list
        dense
        min-width="150"
        max-height="400"
        class="overflow-y-auto"
    >
      <v-list-item @click.stop="showNewLinkTypes">
        <v-list-item-content>
          <v-list-item-title>new relation...</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item
          v-for="(link, i) in sourceChunk.links"
          :key="i"
      >
        <v-list-item-content>
          <v-list-item-subtitle v-text="link.targetLabel"></v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-btn icon @click.stop="deleteLink(link, i)">
            <v-icon color="grey lighten-1">mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-menu>

  <v-menu
      v-else-if="label && activeMenu==='new-link'"
      v-model="showNewLinkMenu"
      offset-y
  >
    <template #activator="{ on }">
      <span :id="'spn-' + spanid" :style="{ borderColor: color }" class="highlight bottom" v-on="on">
        <span class="highlight__content">{{ content }}<v-icon class="delete" @click.stop="remove">mdi-close-circle</v-icon><span
            class="active-link-source" @click.stop="abortNewLink"></span></span><span
          :data-label="label" :style="{ backgroundColor: color, color: textColor }" class="highlight__label"/>
      </span>
    </template>

    <v-list
        dense
        min-width="150"
        max-height="400"
        class="overflow-y-auto"
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>choose relation type:</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item
          v-for="(type, i) in linkTypes"
          :key="i"
          @click="selectNewLinkType(type)"
      >
        <v-list-item-action>
          <v-list-item-action-text v-text="type.name"/>
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
    linkTypes: {
      type: Array,
      default: () => [],
      required: true
    },
    newline: {
      type: Boolean
    },
    sourceChunk: {
      type: Object,
      default: () => {
      }
    },
    sourceLinkType: {
      type: Object,
      default: () => {
      },
      required: true
    }
  },

  data() {
    return {
      showMenu: false,
      showActiveLinksMenu: false,
      showNewLinkMenu: false,
      showChangeLinkMenu: false,
      activeMenu: false
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
      this.closeAllMenus();
    },

    remove() {
      this.$emit('remove')
    },

    closeAllMenus() {
      this.showMenu = false;
      this.showActiveLinksMenu = false;
      this.showNewLinkMenu = false;
      this.showChangeLinkMenu = false;
      this.activeMenu = false;
    },

    showActiveLinks() {
      this.closeAllMenus();
      this.showActiveLinksMenu = true;
      this.activeMenu = 'active-links';
      this.$emit('selectSource');
    },

    showNewLinkTypes() {
      this.closeAllMenus();
      this.activeMenu = 'new-link';
      this.showNewLinkMenu = true;
    },

    deleteLink(link, i) {
      this.$emit('deleteLink', {id: link.id, ndx: i});
    },

    selectNewLinkType(type) {
      this.closeAllMenus();
      this.$emit('selectNewLinkType', type);
    },

    changeLinkType(type) {
      this.closeAllMenus();
      this.$emit('changeLinkType', type);
    },

    selectTarget() {
      this.closeAllMenus();
      this.$emit('selectTarget');
    },

    abortNewLink() {
      this.closeAllMenus();
      this.$emit('hideAllLinkMenus');
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

.highlight .choose-link-type:before {
  content: 'R';
}

.highlight .active-link-source:before {
  content: 'R';
}

.highlight .choose-target:before {
  content: '+';
}

.highlight .choose-link-type,
.highlight .active-link-source,
.highlight .choose-target {
  display: none;
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

.highlight:hover .choose-link-type,
.highlight:hover .choose-target {
  display: block;
}

.highlight .active-link-source {
  display: block;
  background: #00a4cf;
  color: #ffffff;
}

.highlight__content {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 2px 2px 0 6px;
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
