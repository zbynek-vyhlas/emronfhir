import { createPinia } from 'pinia';

export const setupStore = app => {
  app.use(createPinia());
};
