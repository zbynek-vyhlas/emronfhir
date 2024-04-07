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
      path: "/data/",
      name: "data-page",
      component: () => import("@/pages/DataPage.vue"),
    },
    {
      path: "/actions/",
      name: "actions-page",
      component: () => import("@/pages/ActionsPage.vue"),
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
