<template>
  <div>
    <v-annotator
      :dark="$vuetify.theme.dark"
      :rtl="rtl"
      :text="text"
      :entities="JSON.stringify(entities)"
      :entity-labels="entityLabels"
      :relations="relations"
      :relation-labels="relationLabels"
      :allow-overlapping="allowOverlapping"
      :grapheme-mode="graphemeMode"
      @add:entity="handleAddEvent"
      @click:entity="handleEntityClickEvent"
      @click:relation="updateRelation"
      @contextmenu:entity="deleteEntity"
      @contextmenu:relation="deleteRelation"
    />
    <v-menu
      v-model="showMenu"
      :position-x="x"
      :position-y="y"
      absolute
      offset-y
    >
      <v-list
        dense
        min-width="150"
        max-height="400"
        class="overflow-y-auto"
      >
        <v-list-item
          v-for="(label, i) in entityLabels"
          :key="i"
          v-shortkey="[label.suffixKey]"
          @shortkey="addOrUpdateEntity(label.id)"
          @click="addOrUpdateEntity(label.id)"
        >
          <v-list-item-action
            v-if="hasAnySuffixKey"
          >
            <v-chip
              v-if="label.suffixKey"
              :color="label.backgroundColor"
              outlined
              small
              v-text="label.suffixKey"
            />
            <span v-else class="mr-8" />
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="label.text"/>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VAnnotator from 'v-annotator'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

export default Vue.extend({
  components: {
    VAnnotator,
  },

  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    rtl: {
      type: Boolean,
      default: false,
    },
    text: {
      type: String,
      default: "",
      required: true,
    },
    entities: {
      type: Array,
      default: () => [],
      required: true,
    },
    entityLabels: {
      type: Array,
      default: () => [],
      required: true,
    },
    relations: {
      type: Array,
      default: () => [],
    },
    relationLabels: {
      type: Array,
      default: () => [],
    },
    allowOverlapping: {
      type: Boolean,
      default: false,
      required: false,
    },
    graphemeMode: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      showMenu: false,
      x: 0,
      y: 0,
      startOffset: 0,
      endOffset: 0,
      entityId: -1,
    };
  },

  computed: {
    hasAnySuffixKey(): boolean {
      return this.entityLabels.some((label: any) => label.suffixKey !== null)
    }
  },

  methods: {
    setOffset(startOffset: number, endOffset: number) {
      this.startOffset = startOffset
      this.endOffset = endOffset
    },

    setEntity(entityId: number) {
      this.entityId = entityId
    },

    showEntityLabelMenu(e: any) {
      e.preventDefault()
      this.showMenu = false
      this.x = e.clientX || e.changedTouches[0].clientX
      this.y = e.clientY || e.changedTouches[0].clientY
      this.$nextTick(() => {
        this.showMenu = true
      })
    },

    handleAddEvent(e: any, startOffset: number, endOffset: number) {
      this.setOffset(startOffset, endOffset)
      this.showEntityLabelMenu(e)
    },

    handleEntityClickEvent(e: any, entityId: number) {
      this.setEntity(entityId)
      this.showEntityLabelMenu(e)
    },

    addOrUpdateEntity(labelId: number) {
      if (this.entityId !== -1) {
        this.updateEntity(labelId)
      } else {
        this.addEntity(labelId)
      }
      this.showMenu = false
      this.startOffset = 0
      this.endOffset = 0
      this.entityId = -1
    },

    addEntity(labelId: number) {
      this.$emit('addEntity', this.startOffset, this.endOffset, labelId)
    },

    updateEntity(labelId: number) {
      this.$emit('click:entity', this.entityId, labelId)
    },

    deleteEntity(entity: any) {
      this.$emit('contextmenu:entity', entity.id)
    },

    updateRelation() {
      console.log("updateRelation")
    },

    deleteRelation(relation: any) {
      this.$emit('contextmenu:relation', relation.id)
    }
  },
});
</script>
