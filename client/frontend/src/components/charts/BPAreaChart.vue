<template>
  <v-skeleton-loader
    v-if="false"
    class="mx-auto border"
    max-width="800"
    type="table-tbody"
  ></v-skeleton-loader>
  <!-- v-if="!epicData.length" -->
  <v-chart v-else class="chart" :option="option" autoresize />
</template>

<script setup>
import { ref, watchEffect, provide, computed } from 'vue';
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
      data: ['bad compliance', 'good compliance', 'excellent compliance'],
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
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      },
    ],
    yAxis: [
      {
        type: 'value',
      },
    ],
    series: [
      {
        name: 'bad compliance',
        type: 'line',
        stack: 'Total',
        emphasis: {
          focus: 'series',
        },
        data: [120, 132, 101, 134, 90, 230, 210],
        itemStyle: {
          color: '#9BB8CD',
        },
        lineStyle: {
          color: '#9BB8CD',
        },
        areaStyle: {
          color: 'rgba(155, 184, 205, 0.75)',
        },
      },
      {
        name: 'good compliance',
        type: 'line',
        stack: 'Total',
        emphasis: {
          focus: 'series',
        },
        data: [220, 182, 191, 234, 290, 330, 310],
        itemStyle: {
          color: '#EEC759',
        },
        lineStyle: {
          color: '#EEC759',
        },
        areaStyle: {
          color: 'rgba(238, 199, 89, 0.75)',
        },
      },
      {
        name: 'excellent compliance',
        type: 'line',
        stack: 'Total',
        emphasis: {
          focus: 'series',
        },
        data: [150, 232, 201, 154, 190, 330, 410],
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
</script>

<style scoped>
.chart {
  height: 30vh;
}
</style>
