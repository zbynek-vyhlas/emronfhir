<template>
  <div>
    <h1>Dashboard</h1>
  </div>
  <v-row>
    <v-col col="6">
      <v-card class="pa-5" title="Vital Signs">
        <v-skeleton-loader
          class="mx-auto border"
          max-width="300"
          type="image, article"
        ></v-skeleton-loader>
        <!-- <PieChart1></PieChart1> -->
      </v-card>
    </v-col>
    <v-col col="6">
      <v-card class="pa-5" title="Labs">
        <v-skeleton-loader
          class="mx-auto border"
          max-width="300"
          type="image, article"
        ></v-skeleton-loader>
        <!-- <PieChart2></PieChart2> -->
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Medications">
        <v-skeleton-loader
          class="mx-auto border"
          max-width="300"
          type="image, article"
        ></v-skeleton-loader>
        <!-- <StackedAreaChart></StackedAreaChart> -->
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import PieChart1 from '../components/charts/PieChart1.vue';
import PieChart2 from '../components/charts/PieChart2.vue';
import StackedAreaChart from '../components/charts/StackedAreaChart.vue';

export default {
  components: {
    PieChart1,
    PieChart2,
    StackedAreaChart,
  },
};
</script>
