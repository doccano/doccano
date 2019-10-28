<template>
  <base-card
    :title="title"
    :agree-text="buttonTrueText"
    :cancel-text="buttonFalseText"
    @agree="ok"
    @cancel="cancel"
  >
    <template #content>
      {{ message }}
      <v-list dense>
        <v-list-item v-for="(item, i) in items" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ item[itemKey] }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    BaseCard
  },

  props: {
    title: {
      type: String,
      default: '',
      required: true
    },
    message: {
      type: String,
      default: '',
      required: true
    },
    items: {
      type: Array,
      default: () => [],
      required: true
    },
    itemKey: {
      type: String,
      default: '',
      required: true
    },
    buttonTrueText: {
      type: String,
      default: 'Yes'
    },
    buttonFalseText: {
      type: String,
      default: 'Cancel'
    }
  },

  methods: {
    ok() {
      this.$emit('ok')
    },
    cancel() {
      this.$emit('cancel')
    }
  }
}
</script>
