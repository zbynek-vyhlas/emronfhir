<template>
  <div>
    <h1>Dashboard</h1>
  </div>
  <v-row>
    <v-col col="6">
      <v-card class="pa-5" title="Customers">
        <PieChart1></PieChart1>
      </v-card>
    </v-col>
    <v-col col="6">
      <v-card class="pa-5" title="Customers">
        <PieChart2></PieChart2>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Customers">
        <StackedAreaChart></StackedAreaChart>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import PieChart1 from "../components/charts/PieChart1.vue";
import PieChart2 from "../components/charts/PieChart2.vue";
import StackedAreaChart from "../components/charts/StackedAreaChart.vue";

export default {
  components: {
    PieChart1,
    PieChart2,
    StackedAreaChart,
  },
};
</script>
