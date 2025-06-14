<template>
  <v-card>
    <v-card-title v-text="title" />
    <v-divider />
    <v-tabs show-arrows>
      <v-tab v-for="(value, user) in chartJSFormat" :key="user" class="text-capitalize">
        {{ user }}
      </v-tab>
      <v-tab-item v-for="(value, user) in chartJSFormat" :key="user">
        <v-card-text>
          <bar-chart :chart-data="value" />
        </v-card-text>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'
import BarChart from '@/components/metrics/ChartBar.vue'
import { Distribution } from '~/domain/models/metrics/metrics'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  components: {
    BarChart
  },

  props: {
    title: {
      type: String,
      required: true,
      default: 'Distribution'
    },
    distribution: {
      type: Object as PropType<Distribution>,
      required: true
    },
    labelTypes: {
      type: Array as PropType<LabelDTO[]>,
      default: () => [],
      required: true
    }
  },

  computed: {
    colorMapping(): { [text: string]: string } {
      return Object.fromEntries(
        this.labelTypes.map((labelType) => [labelType.text, labelType.backgroundColor])
      )
    },

    chartJSFormat(): any {
      const data: { [user: string]: { labels: string[]; datasets: any[] } } = {}
      for (const user in this.distribution) {
        const labels = Object.keys(this.distribution[user])
        labels.sort()
        const counts = labels.map((label) => this.distribution[user][label])
        const colors = labels.map((label) =>
          label in this.colorMapping ? this.colorMapping[label] : '#00d1b2'
        )
        data[user] = {
          labels,
          datasets: [
            {
              title: this.title,
              backgroundColor: colors,
              data: counts
            }
          ]
        }
      }
      return data
    }
  }
})
</script>
