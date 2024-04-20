<template>
  <div>
    <h1>Vital Signs</h1>
  </div>

  <v-row justify="center">
    <v-col cols="8">
      <v-skeleton-loader
        class="mx-auto border"
        max-width="600"
        type="table-thead, table-tbody"
      ></v-skeleton-loader>
      <!-- <v-card
        ><v-card-title>Vital Signs</v-card-title>
        <v-card-text>
          <v-table fixed-header height="300px">
            <thead>
              <tr>
                <th class="text-left">Name</th>
                <th class="text-left">value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in companies" :key="item.name">
                <td>{{ item.name }}</td>
                <td>{{ item.value }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card> -->
    </v-col>
  </v-row>
</template>
<script>
export default {
  data() {
    return {
      companies: [
        {
          name: 'datapoint 1',
          value: 262,
        },
        {
          name: 'datapoint 2',
          value: 305,
        },
        {
          name: 'datapoint 3',
          value: 356,
        },
        {
          name: 'datapoint 4',
          value: 375,
        },
        {
          name: 'datapoint 5',
          value: 392,
        },
        {
          name: 'datapoint 6',
          value: 408,
        },
        {
          name: 'datapoint 7',
          value: 452,
        },
        {
          name: 'datapoint 8',
          value: 518,
        },
      ],
    };
  },
};
</script>
