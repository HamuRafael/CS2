import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import CompareView from "../views/CompareView.vue";
import HistoryView from "../views/HistoryView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/compare", name: "compare", component: CompareView },
  { path: "/history", name: "history", component: HistoryView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
