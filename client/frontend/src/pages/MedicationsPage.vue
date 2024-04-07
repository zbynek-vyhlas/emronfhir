<template>
  <div>
    <h1>Medications</h1>
  </div>

  <v-row justify="center">
    <v-col cols="8"
      ><v-card
        ><v-card-title>Medications</v-card-title>
        <v-card-text>
          <v-table fixed-header height="300px">
            <thead>
              <tr>
                <th class="text-left">Name</th>
                <th class="text-left">Products</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in companies" :key="item.name">
                <td>{{ item.name }}</td>
                <td>{{ item.products }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
export default {
  data() {
    return {
      companies: [
        {
          name: "Compandy 1",
          products: 262,
        },
        {
          name: "Compandy 2",
          products: 305,
        },
        {
          name: "Compandy 3",
          products: 356,
        },
        {
          name: "Compandy 4",
          products: 375,
        },
        {
          name: "Compandy 5",
          products: 392,
        },
        {
          name: "Compandy 6",
          products: 408,
        },
        {
          name: "Compandy 7",
          products: 452,
        },
        {
          name: "Compandy 8",
          products: 518,
        },
      ],
    };
  },
};
</script>
