<template>
  <div>
    <v-annotator
      :dark="$vuetify.theme.dark"
      :rtl="rtl"
      :text="text"
      :entities="entities"
      :entity-labels="entityLabels"
      :relations="relations"
      :relation-labels="relationLabels"
      :allow-overlapping="allowOverlapping"
      :grapheme-mode="graphemeMode"
      @add:entity="handleAddEvent"
      @click:entity="onEntityClicked"
      @click:relation="onRelationClicked"
      @contextmenu:entity="deleteEntity"
      @contextmenu:relation="deleteRelation"
    />
    <labeling-menu
      :opened="entityMenuOpened"
      :x="x"
      :y="y"
      :selected-label="currentLabel"
      :labels="entityLabels"
      @close="cleanUp"
      @click:label="addOrUpdateEntity"
    />
    <labeling-menu
      :opened="relationMenuOpened"
      :x="x"
      :y="y"
      :selected-label="currentRelationLabel"
      :labels="relationLabels"
      @close="cleanUp"
      @click:label="addOrUpdateRelation"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VAnnotator from 'v-annotator'
import LabelingMenu from './LabelingMenu.vue'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

export default Vue.extend({
  components: {
    VAnnotator,
    LabelingMenu,
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
    selectedLabel: {
      type: Object,
      default: null,
      required: false,
    },
    relationMode: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      entityMenuOpened: false,
      relationMenuOpened: false,
      x: 0,
      y: 0,
      startOffset: 0,
      endOffset: 0,
      entity: null as any,
      relation: null as any,
      fromEntity: null as any,
      toEntity: null as any,
    };
  },

  computed: {
    currentLabel(): any {
      if (this.entity) {
        const label = this.entityLabels.find((label: any) => label.id === this.entity!.label)
        return label
      } else {
        return null
      }
    },

    currentRelationLabel(): any {
      if (this.relation) {
        const label = this.relationLabels.find((label: any) => label.id === this.relation.labelId)
        return label
      } else {
        return null
      }
    }
  },

  methods: {
    setOffset(startOffset: number, endOffset: number) {
      this.startOffset = startOffset
      this.endOffset = endOffset
    },

    setEntity(entityId: number) {
      this.entity = this.entities.find((entity: any) => entity.id === entityId)
    },

    setRelation(relationId: number) {
      this.relation = this.relations.find((relation: any) => relation.id === relationId)
    },

    setEntityForRelation(e: any, entityId: number) {
      const entity = this.entities.find((entity: any) => entity.id === entityId)
      if (!this.fromEntity) {
        this.fromEntity = entity
      } else {
        this.toEntity = entity
        if (this.selectedLabel) {
          this.addRelation(this.selectedLabel.id)
        } else {
          this.showRelationLabelMenu(e)
        }
      }
    },

    showEntityLabelMenu(e: any) {
      e.preventDefault()
      this.entityMenuOpened = false
      this.x = e.clientX || e.changedTouches[0].clientX
      this.y = e.clientY || e.changedTouches[0].clientY
      this.$nextTick(() => {
        this.entityMenuOpened = true
      })
    },

    showRelationLabelMenu(e: any) {
      e.preventDefault()
      this.relationMenuOpened = false
      this.x = e.clientX || e.changedTouches[0].clientX
      this.y = e.clientY || e.changedTouches[0].clientY
      this.$nextTick(() => {
        this.relationMenuOpened = true
      })
    },

    handleAddEvent(e: any, startOffset: number, endOffset: number) {
      this.setOffset(startOffset, endOffset)
      if (this.selectedLabel) {
        this.addOrUpdateEntity(this.selectedLabel.id)
      } else {
        this.showEntityLabelMenu(e)
      }
    },

    onEntityClicked(e: any, entityId: number) {
      if (this.relationMode) {
        this.setEntityForRelation(e, entityId)
      } else {
        this.setEntity(entityId)
        this.showEntityLabelMenu(e)
      }
    },

    onRelationClicked(e: any, relation: any) {
      this.setRelation(relation.id)
      this.showRelationLabelMenu(e)
    },

    addOrUpdateEntity(labelId: number) {
      if (labelId) {
        if (this.entity) {
          this.updateEntity(labelId)
        } else {
          this.addEntity(labelId)
        }
      } else {
        this.deleteEntity(this.entity)
      }
      this.cleanUp()
    },

    addOrUpdateRelation(labelId: number) {
      if (labelId) {
        if (this.relation) {
          this.updateRelation(labelId)
        } else {
          this.addRelation(labelId)
        }
      } else {
        this.deleteRelation(this.relation)
      }
      this.cleanUp()
    },

    addEntity(labelId: number) {
      this.$emit('addEntity', this.startOffset, this.endOffset, labelId)
    },

    updateEntity(labelId: number) {
      this.$emit('click:entity', this.entity!.id, labelId)
    },

    deleteEntity(entity: any) {
      this.$emit('contextmenu:entity', entity.id)
      this.cleanUp()
    },

    cleanUp() {
      this.entityMenuOpened = false
      this.relationMenuOpened = false
      this.entity = null
      this.relation = null
      this.startOffset = 0
      this.endOffset = 0
    },

    addRelation(labelId: number) {
      this.$emit('addRelation', this.fromEntity.id, this.toEntity.id, labelId)
      this.fromEntity = null
      this.toEntity = null
    },

    updateRelation(labelId: number) {
      this.$emit("click:relation", this.relation.id, labelId)
    },

    deleteRelation(relation: any) {
      this.$emit('contextmenu:relation', relation.id)
    }
  },
});
</script>
