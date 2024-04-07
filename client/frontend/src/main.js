import "@/assets/main.css";

import { createApp } from "vue";
import App from "@/App.vue";
import { setupStore } from "@/stores";
import router from "@/router";
import vuetify from "@/plugins/vuetify";

const app = createApp(App);
setupStore(app);
app.use(vuetify);
app.use(router);

app.mount("#app");
