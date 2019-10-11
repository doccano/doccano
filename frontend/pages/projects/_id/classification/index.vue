<template>
  <div>
    <side-bar-labeling
      :labels="labels"
      :progress="progress"
      :metadata="metadata"
    />
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center>
          <v-flex>
            <text-classification />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import TextClassification from '~/components/containers/TextClassification'
import SideBarLabeling from '~/components/organisms/SideBarLabeling'

export default {
  layout: 'annotation',

  components: {
    TextClassification,
    SideBarLabeling
  },

  data() {
    return {
      progress: 30,
      metadata: '{"wikiPageId":2}',
      labels: [
        {
          id: 1,
          name: 'Location',
          color: '#E91E63',
          shortcut: 'l'
        },
        {
          id: 2,
          name: 'Organization',
          color: '#03A9F4',
          shortcut: 'o'
        },
        {
          id: 3,
          name: 'Person',
          color: '#009688',
          shortcut: 'p'
        },
        {
          id: 4,
          name: 'Date',
          color: '#FF6F00',
          shortcut: 'd'
        },
        {
          id: 5,
          name: 'Other',
          color: '#333333',
          shortcut: 't'
        }
      ]
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
