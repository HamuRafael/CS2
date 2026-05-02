<template>
  <div class="min-h-screen">
    <header class="px-6 py-6 md:px-12">
      <div class="mx-auto flex max-w-6xl items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="h-10 w-10 rounded-full bg-ember/80"></div>
          <div>
            <p class="text-xs uppercase tracking-[0.4em] text-fog/60">CS2</p>
            <h1 class="text-xl font-semibold">Stat Clash</h1>
          </div>
        </div>
        <nav class="hidden gap-6 text-sm md:flex">
          <RouterLink class="hover:text-ember" to="/">Compare</RouterLink>
          <RouterLink class="hover:text-ember" to="/history">History</RouterLink>
        </nav>
      </div>
    </header>

    <main class="px-6 pb-16 md:px-12">
      <div class="mx-auto max-w-6xl">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>
