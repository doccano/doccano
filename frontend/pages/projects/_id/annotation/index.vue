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
            <v-card>
              <v-card-text class="title">
                <entity-item-container :content="text" :labels="labels" :entities="annotations" />
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import EntityItemContainer from '~/components/EntityItemContainer'
import SideBarLabeling from '~/components/project/SideBarRight/SideBarLabeling'

export default {
  layout: 'annotation',
  components: {
    EntityItemContainer,
    SideBarLabeling
  },
  data: () => ({
    progress: 30,
    metadata: '{"wikiPageId":2}',
    search: '',
    content: 'Sony',
    text:
      'Barack Hussein Obama II (born August 4, 1961) is an American attorney and politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African American to be elected to the presidency. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004.',
    labelName: 'ORG',
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
    ],
    annotations: [
      {
        id: 2,
        prob: 0.0,
        label: 3,
        start_offset: 0,
        end_offset: 23,
        user: 1,
        document: 1
      },
      {
        id: 3,
        prob: 0.0,
        label: 4,
        start_offset: 30,
        end_offset: 44,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 1,
        start_offset: 125,
        end_offset: 138,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 4,
        start_offset: 144,
        end_offset: 148,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 4,
        start_offset: 152,
        end_offset: 156,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 2,
        start_offset: 174,
        end_offset: 190,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 1,
        start_offset: 285,
        end_offset: 289,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 1,
        start_offset: 303,
        end_offset: 311,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 4,
        start_offset: 317,
        end_offset: 321,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 4,
        start_offset: 325,
        end_offset: 329,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 1,
        start_offset: 337,
        end_offset: 345,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 4,
        start_offset: 365,
        end_offset: 369,
        user: 1,
        document: 1
      },
      {
        id: 2,
        prob: 0.0,
        label: 4,
        start_offset: 373,
        end_offset: 377,
        user: 1,
        document: 1
      }
    ]
  }),

  methods: {
    save() {},
    cancel() {},
    open() {},
    close() {}
  }
}
</script>

<style scoped>
</style>
