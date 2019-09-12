<template>
  <base-text-area>
    <template #title>
      <multi-class-classification
        :labels="items"
      />
    </template>
    <template #content>
      <div class="title">
        Text area
      </div>
    </template>
  </base-text-area>
</template>

<script>
import BaseTextArea from '@/components/molecules/BaseTextArea'
import MultiClassClassification from '@/components/organisms/MultiClassClassification'

export default {
  components: {
    BaseTextArea,
    MultiClassClassification
  },

  computed: {
    items() {
      return ['foo', 'bar']
    }
  },

  created() {
  },

  methods: {
  }
}
</script>
