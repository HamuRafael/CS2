<template>
  <section class="grid gap-8 md:grid-cols-[1.1fr_0.9fr]">
    <div class="space-y-6">
      <div class="fade-in">
        <p class="text-xs uppercase tracking-[0.4em] text-fog/60">Compare CS2 talent</p>
        <h2 class="text-4xl md:text-5xl">Read the match-up before you queue.</h2>
        <p class="mt-4 text-base text-fog/70">
          Paste two Steam profile URLs and get a clean, visual breakdown of aim, utility, clutch, and
          map performance. Powered by public Leetify data.
        </p>
      </div>
      <SteamCompareForm />
    </div>
    <div class="glass fade-in rounded-2xl p-6">
      <h3 class="text-lg font-semibold">What you will see</h3>
      <ul class="mt-4 space-y-3 text-sm text-fog/70">
        <li>Side-by-side scorelines for every available metric.</li>
        <li>Instant highlights for who owns aim, clutch, and utility.</li>
        <li>Recent match trends and map flavor when data exists.</li>
        <li>Saved comparisons so you can revisit later.</li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import SteamCompareForm from "../components/SteamCompareForm.vue";
</script>
