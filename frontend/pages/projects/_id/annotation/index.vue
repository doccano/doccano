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
            <v-card color="transparent elevation-0">
              <v-card-title>
                <guideline-button />
              </v-card-title>
            </v-card>
            <v-card>
              <v-card-text class="title">
                <entity-item-box />
              </v-card-text>
            </v-card>
            <paginator class="mt-3" />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import EntityItemBox from '~/components/containers/EntityItemBox'
import SideBarLabeling from '~/components/organisms/SideBarLabeling'
import Paginator from '~/components/containers/Paginator'
import GuidelineButton from '@/components/containers/GuidelineButton'

export default {
  layout: 'annotation',

  components: {
    EntityItemBox,
    SideBarLabeling,
    Paginator,
    GuidelineButton
  },

  data() {
    return {
      progress: 30,
      metadata: '{"wikiPageId":2}',
      page: 1,
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
