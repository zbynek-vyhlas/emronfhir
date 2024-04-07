<template>
  <h1>Actions page</h1>
  <v-row>
    <v-col v-for="n in 4" :key="n" cols="6">
      <v-card
        :title="`Content ${n}`"
        :subtitle="`Subtitle for Content ${n}`"
        text="Lorem ipsum dolor sit amet consectetur, adipisicing elit.?"
      >
        <v-card-actions>
          <v-spacer />
          <v-btn variant="tonal" color="secondary"> cancel </v-btn>
          <v-btn variant="tonal" color="primary"> more info </v-btn>
          <v-btn variant="tonal" color="tertiary"> confirm </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>
