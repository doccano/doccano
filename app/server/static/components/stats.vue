<template lang="pug">
  div(v-cloak="")
    div.columns
      div.column.is-12
        div.card

          header.card-header
            p.card-header-title Label stats
            a.card-header-icon(href="#", aria-label="more options")
              span.icon
                i.fas.fa-angle-down(aria-hidden="true")

          div.card-content.columns
            div.column.is-8
              line-chart(v-bind:chart-data="labelData")
            div.column.is-4
              h2.subtitle Annotation Progress
              doughnut-chart(v-bind:chart-data="progressData")

    div.columns
      div.column.is-8
        div.card

          header.card-header
            p.card-header-title User stats
            a.card-header-icon(href="#", aria-label="more options")
              span.icon
                i.fas.fa-angle-down(aria-hidden="true")

          div.card-content
            line-chart(v-bind:chart-data="userData")
</template>

<script>
import HorizontalBar from 'vue-chartjs/es/BaseCharts/HorizontalBar';
import Doughnut from 'vue-chartjs/es/BaseCharts/Doughnut';
import reactiveProp from 'vue-chartjs/es/mixins/reactiveProp';
import HTTP from './http';

const LineChart = {
  extends: HorizontalBar,

  mixins: [reactiveProp],

  props: {
    chartData: {
      type: Object,
      default: () => {},
    },
  },

  data: () => ({
    options: {
      scales: {
        yAxes: [{
          barPercentage: 0.3,
        }],
        xAxes: [{
          ticks: {
            beginAtZero: true,
            min: 0,
          },
        }],
      },
      maintainAspectRatio: false,
    },
  }),

  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};


const DoughnutChart = {
  extends: Doughnut,

  mixins: [reactiveProp],

  props: {
    chartData: {
      type: Object,
      default: () => {},
    },
  },

  data: () => ({
    options: {
      maintainAspectRatio: false,
    },
  }),

  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};

export default {
  components: { LineChart, DoughnutChart },

  data: () => ({
    labelData: null,
    userData: null,
    progressData: null,
  }),

  created() {
    HTTP.get('statistics').then((response) => {
      this.labelData = this.makeData(response.data.label, 'Label stats');
      this.userData = this.makeData(response.data.user, 'User stats');
      const complete = response.data.total - response.data.remaining;
      const incomplete = response.data.remaining;
      this.progressData = {
        datasets: [{
          data: [complete, incomplete],
          backgroundColor: ['#00d1b2', '#ffdd57'],
        }],

        labels: [
          'Completed',
          'Incomplete',
        ],
      };
    });
  },

  methods: {
    makeData(object, label) {
      const labels = Object.keys(object);
      const counts = Object.values(object);
      const res = {
        labels: labels,
        datasets: [{
          label: label,
          backgroundColor: '#00d1b2',
          data: counts,
        }],
      };
      return res;
    },
  },
};
</script>
