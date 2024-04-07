import { createRouter, createWebHistory } from "vue-router";

export default new createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/reset-your-password-here/",
      name: "password-reset-page",
      component: () => import("@/pages/ResetPasswordPage.vue"),
      meta: { isPublic: true },
    },
    {
      path: "/",
      name: "home-page",
      redirect: { name: "dashboard-page" },
    },
    {
      path: "/dashboard/",
      name: "dashboard-page",
      component: () => import("@/pages/DashboardPage.vue"),
    },
    {
      path: "/medications/",
      name: "medications-page",
      component: () => import("@/pages/MedicationsPage.vue"),
    },
    {
      path: "/labs/",
      name: "labs-page",
      component: () => import("@/pages/LabsPage.vue"),
    },
    {
      path: "/vitals/",
      name: "vitals-page",
      component: () => import("@/pages/VitalsPage.vue"),
    },
    {
      path: "/user/",
      name: "user-page",
      component: () => import("@/pages/UserPage.vue"),
    },
    {
      path: "/settings/",
      name: "settings-page",
      component: () => import("@/pages/SettingsPage.vue"),
    },
  ],
});
