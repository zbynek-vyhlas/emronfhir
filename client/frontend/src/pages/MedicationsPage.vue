<template>
  <div>
    <h1>Medications</h1>
  </div>

  <v-row justify="center">
    <v-col cols="8">
      <v-skeleton-loader
        v-if="!medications.length"
        class="mx-auto border"
        max-width="800"
        type="table-thead, table-tbody"
      ></v-skeleton-loader>
      <v-card v-else
        ><v-card-title>Medications</v-card-title>
        <v-card-text>
          <v-table fixed-header height="300px">
            <thead>
              <tr>
                <th class="text-left">Name</th>
                <th class="text-left">Dosage</th>
                <th class="text-left">Instructions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="medication in medications" :key="medication.name">
                <td>{{ medication.name }}</td>
                <td>{{ medication.dosage }}</td>
                <td>{{ medication.instructions }}</td>
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
export default {
  data() {
    return {
      medications: [],
    };
  },
  methods: {
    async loadMedications() {
      const epicAccessToken = Cookies.get('epic_access_token');
      if (epicAccessToken) {
        axios
          .get(import.meta.env.VITE_FHIR_BASE_URL + '/MedicationRequest', {
            headers: {
              Authorization: `Bearer ${epicAccessToken}`,
            },
          })
          .then((response) => {
            // I need to separate the medications and dosages
            const regex = / (?=\d)/;
            for (let medication of response.data.entry) {
              const medicationRecord =
                medication.resource.medicationReference?.display;
              if (medicationRecord) {
                const parsedMedications = medicationRecord.split(regex);
                this.medications.push({
                  name: parsedMedications[0],
                  dosage: parsedMedications[1],
                  instructions:
                    medication.resource.dosageInstruction[0].patientInstruction,
                });
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
    this.loadMedications();
  },
};
</script>
