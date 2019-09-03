<template>
  <label-list
    :headers="headers"
    :labels="items"
    :selected="selected"
    @update-selected="updateSelected"
    @update-label="handleUpdateLabel"
  />
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'
import LabelList from '@/components/organisms/LabelList'

export default {
  components: {
    LabelList
  },
  data() {
    return {
      headers: [
        {
          text: 'Name',
          align: 'left',
          value: 'text'
        },
        {
          text: 'Shortkey',
          value: 'suffix_key'
        },
        {
          text: 'Color',
          sortable: false,
          value: 'background_color'
        }
      ]
    }
  },

  computed: {
    ...mapState('labels', ['items', 'selected'])
  },

  created() {
    this.getLabelList()
  },

  methods: {
    ...mapActions('labels', ['getLabelList', 'updateLabel']),
    ...mapMutations('labels', ['updateSelected']),

    handleUpdateLabel(payload) {
      const data = {
        projectId: this.$route.params.id,
        ...payload
      }
      this.updateLabel(data)
    }
  }
}
</script>
