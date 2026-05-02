<template>
  <form class="glass fade-in rounded-2xl p-6 md:p-8" @submit.prevent="onSubmit">
    <div class="grid gap-6 md:grid-cols-2">
      <div>
        <label class="text-xs uppercase tracking-[0.3em] text-fog/60">Your Steam Profile URL</label>
        <input
          v-model.trim="playerAUrl"
          class="mt-2 w-full rounded-xl border border-fog/20 bg-ink/70 px-4 py-3 text-fog placeholder:text-fog/40"
          type="url"
          placeholder="https://steamcommunity.com/profiles/..."
          required
        />
      </div>
      <div>
        <label class="text-xs uppercase tracking-[0.3em] text-fog/60">Opponent / Friend Steam Profile URL</label>
        <input
          v-model.trim="playerBUrl"
          class="mt-2 w-full rounded-xl border border-fog/20 bg-ink/70 px-4 py-3 text-fog placeholder:text-fog/40"
          type="url"
          placeholder="https://steamcommunity.com/id/..."
          required
        />
      </div>
    </div>

    <div class="mt-6 flex flex-wrap items-center gap-4">
      <button
        class="rounded-xl bg-ember px-6 py-3 font-semibold text-ink shadow-lg shadow-ember/30 hover:-translate-y-0.5"
        type="submit"
        :disabled="loading"
      >
        {{ loading ? "Comparing..." : "Compare" }}
      </button>
      <p class="text-sm text-fog/60">Paste two Steam profile URLs to compare CS2 performance.</p>
    </div>

    <ErrorMessage v-if="error" class="mt-4" :message="error" />
  </form>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useComparisonStore } from "../stores/comparisonStore";
import ErrorMessage from "./ErrorMessage.vue";

const router = useRouter();
const store = useComparisonStore();
const playerAUrl = ref("");
const playerBUrl = ref("");

const loading = computed(() => store.loading);
const error = computed(() => store.error);

async function onSubmit() {
  if (!playerAUrl.value || !playerBUrl.value) {
    return;
  }
  try {
    await store.comparePlayers(playerAUrl.value, playerBUrl.value);
    router.push("/compare");
  } catch (error) {
    // Error state handled in store
  }
}
</script>
