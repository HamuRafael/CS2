import { defineStore } from "pinia";
import api from "../services/api";

export const useComparisonStore = defineStore("comparison", {
  state: () => ({
    loading: false,
    error: null,
    comparison: null,
    history: [],
  }),
  actions: {
    async comparePlayers(playerAUrl, playerBUrl) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.post("/api/compare", { playerAUrl, playerBUrl });
        this.comparison = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || "Comparison failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async fetchHistory() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get("/api/comparisons");
        this.history = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || "Failed to load history.";
      } finally {
        this.loading = false;
      }
    },
    async fetchComparisonById(comparisonId) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`/api/comparisons/${comparisonId}`);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || "Failed to load comparison.";
        throw error;
      } finally {
        this.loading = false;
      }
    },
  },
});
