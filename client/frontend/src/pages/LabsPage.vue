<template>
  <div>
    <h1>Lab Reports</h1>
  </div>

  <v-row justify="center">
    <v-col cols="8">
      <v-skeleton-loader
        v-if="!labs.length"
        class="mx-auto border"
        max-width="800"
        type="table-thead, table-tbody"
      ></v-skeleton-loader>
      <v-card v-else
        ><v-card-title>Observations</v-card-title>
        <v-card-text>
          <v-table fixed-header height="300px">
            <thead>
              <tr>
                <th class="text-left">Name</th>
                <th class="text-left">Issued</th>
                <th class="text-left">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in labs" :key="report.name">
                <td>{{ report.title }}</td>
                <td>{{ report.issued }}</td>
                <td>{{ report.value }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import axios from '@/libs/axios';
import Cookies from 'js-cookie';
import { parseISO, format } from 'date-fns';

export default {
  data() {
    return {
      labs: [],
    };
  },
  methods: {
    async loadObservations() {
      const epicAccessToken = Cookies.get('epic_access_token');
      if (epicAccessToken) {
        axios
          .get(
            import.meta.env.VITE_FHIR_BASE_URL +
              '/Observation?category=laboratory',
            {
              headers: {
                Authorization: `Bearer ${epicAccessToken}`,
              },
            }
          )
          .then((response) => {
            for (let entry of response.data.entry) {
              const labTitle = entry.resource.code?.text;
              const issued = entry.resource.issued;
              const value = entry.resource.valueQuantity?.value;

              if (labTitle) {
                let report = {
                  title: labTitle,
                };
                if (issued) {
                  report.issued = format(parseISO(issued), 'MM/dd/yyyy');
                }
                if (value) {
                  report.value = value;
                }
                this.labs.push(report);
              }
            }
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
      } else {
        console.error('epicAccessToken not found');
      }
    },
  },

  mounted() {
    this.loadObservations();
  },
};
</script>
