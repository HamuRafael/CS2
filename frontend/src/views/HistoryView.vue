<template>
  <section class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-xs uppercase tracking-[0.4em] text-fog/60">Recent comparisons</p>
        <h2 class="text-3xl">History</h2>
      </div>
      <button
        class="rounded-xl border border-fog/20 px-4 py-2 text-sm text-fog/70 hover:border-ember"
        @click="store.fetchHistory"
      >
        Refresh
      </button>
    </div>

    <div v-if="store.loading" class="glass rounded-2xl p-6">
      <LoadingSpinner />
    </div>

    <div v-else class="glass rounded-2xl p-6">
      <div v-if="!store.history.length" class="text-sm text-fog/60">
        No comparisons yet.
      </div>
      <ul v-else class="space-y-3 text-sm">
        <li
          v-for="item in store.history"
          :key="item.comparisonId"
          class="flex items-center justify-between border-b border-fog/10 pb-3"
        >
          <span>Comparison #{{ item.comparisonId }}</span>
          <span class="text-fog/60">{{ formatDate(item.createdAt) }}</span>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from "vue";
import { useComparisonStore } from "../stores/comparisonStore";
import LoadingSpinner from "../components/LoadingSpinner.vue";

const store = useComparisonStore();

onMounted(() => {
  store.fetchHistory();
});

function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}
</script>
