<template>
  <base-modal
    text="Delete"
    :disabled="disabled"
  >
    <template v-slot="slotProps">
      <base-card
        :title="title"
        :agree-text="buttonTrueText"
        :cancel-text="buttonFalseText"
        @agree="ok(); slotProps.close()"
        @cancel="slotProps.close"
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
  </base-modal>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'
import BaseModal from '@/components/molecules/BaseModal'

export default {
  components: {
    BaseCard,
    BaseModal
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
    disabled: {
      type: Boolean,
      default: false
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
    }
  }
}
</script>
