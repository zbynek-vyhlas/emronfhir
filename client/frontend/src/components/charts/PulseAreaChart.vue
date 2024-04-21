<template>
  <v-skeleton-loader
    v-if="!epicData.length"
    class="mx-auto border"
    max-width="800"
    type="table-tbody"
  ></v-skeleton-loader>
  <v-chart v-else class="chart" :option="option" autoresize />
</template>

<script setup>
import { ref, onMounted, watchEffect, provide, computed } from 'vue';
import { useTheme } from 'vuetify';
import VChart, { THEME_KEY } from 'vue-echarts';
import { use } from 'echarts/core';
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

import axios from 'axios';
import Cookies from 'js-cookie';
use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition,
]);

const option = ref({});
const epicData = ref([]);
const appTheme = useTheme();
const chartTheme = computed(() =>
  appTheme.global.current.value.dark ? 'dark' : 'light'
);
provide(THEME_KEY, chartTheme);

watchEffect(() => {
  updateChartOptions(chartTheme.value);
});

const loadObservations = async () => {
  const epicAccessToken = Cookies.get('epic_access_token');
  if (epicAccessToken) {
    try {
      const response = await axios.get(
        `${
          import.meta.env.VITE_FHIR_BASE_URL
        }/Observation?category=vital-signs`,
        {
          headers: {
            Authorization: `Bearer ${epicAccessToken}`,
          },
        }
      );

      response.data.entry.forEach((vitalSign) => {
        const vitalSignTitle = vitalSign.resource.code?.text;
        const unit = vitalSign.resource.valueQuantity?.unit;

        if (vitalSignTitle && vitalSignTitle === 'Pulse' && unit === '/min') {
          const value = vitalSign.resource.valueQuantity?.value;
          epicData.value.push(value);
        }
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  } else {
    console.error('epicAccessToken not found');
  }
};

function updateChartOptions(theme) {
  option.value = {
    title: {
      // text: "Title of the chart",
    },
    backgroundColor: theme === 'dark' ? 'black' : null,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985',
        },
      },
    },
    legend: {
      data: ['/min'],
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
        // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      },
    ],
    yAxis: [
      {
        type: 'value',
      },
    ],
    series: [
      {
        name: '/min',
        type: 'line',
        stack: 'Total',
        emphasis: {
          focus: 'series',
        },
        data: epicData.value,
        itemStyle: {
          color: '#B1C381',
        },
        lineStyle: {
          color: '#B1C381',
        },
        areaStyle: {
          color: 'rgba(177, 195, 129, 0.75)',
        },
      },
    ],
  };
}

onMounted(() => {
  loadObservations();
});
</script>

<style scoped>
.chart {
  height: 30vh;
}
</style>
