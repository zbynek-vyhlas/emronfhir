<template>
  <div>
    <h1>Dashboard</h1>
  </div>
  <v-row>
    <v-col col="6">
      <v-card class="pa-5" title="Vital Signs">
        <PieChart1></PieChart1>
      </v-card>
    </v-col>
    <v-col col="6">
      <v-card class="pa-5" title="Labs">
        <PieChart2></PieChart2>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Pulse">
        <PulseAreaChart></PulseAreaChart>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card class="pa-5" title="Blood Pressure">
        <BPAreaChart></BPAreaChart>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import PieChart1 from '../components/charts/PieChart1.vue';
import PieChart2 from '../components/charts/PieChart2.vue';
import PulseAreaChart from '../components/charts/PulseAreaChart.vue';
import BPAreaChart from '../components/charts/BPAreaChart.vue';

export default {
  components: {
    PieChart1,
    PieChart2,
    PulseAreaChart,
    BPAreaChart,
  },
  data() {
    return {
      epicData: [],
    };
  },
};
</script>
