<template>
  <section class="space-y-8">
    <SteamCompareForm />

    <div v-if="store.loading" class="glass rounded-2xl p-6">
      <LoadingSpinner />
    </div>

    <div v-if="comparison" class="space-y-6">
      <div class="grid gap-6 md:grid-cols-2">
        <PlayerCard
          :name="comparison.players.playerA.displayName"
          :steam-id="comparison.players.playerA.steamId"
          :avatar="comparison.players.playerA.avatarUrl"
        />
        <PlayerCard
          :name="comparison.players.playerB.displayName"
          :steam-id="comparison.players.playerB.steamId"
          :avatar="comparison.players.playerB.avatarUrl"
        />
      </div>

      <div class="grid gap-6 md:grid-cols-[1.2fr_0.8fr]">
        <StatComparisonTable :stats="comparison.stats" />
        <StatChart :stats="comparison.stats" />
      </div>

      <div class="glass rounded-2xl p-6">
        <h3 class="text-lg font-semibold">Summary</h3>
        <ul class="mt-3 space-y-2 text-sm text-fog/70">
          <li v-for="(item, index) in comparison.summary" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import { useComparisonStore } from "../stores/comparisonStore";
import LoadingSpinner from "../components/LoadingSpinner.vue";
import PlayerCard from "../components/PlayerCard.vue";
import StatComparisonTable from "../components/StatComparisonTable.vue";
import StatChart from "../components/StatChart.vue";
import SteamCompareForm from "../components/SteamCompareForm.vue";

const store = useComparisonStore();
const comparison = computed(() => store.comparison);
</script>
