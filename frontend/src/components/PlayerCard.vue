<template>
  <div class="glass rounded-2xl p-5">
    <div class="flex items-center gap-4">
      <div class="h-14 w-14 overflow-hidden rounded-full bg-ink/60">
        <img v-if="avatar" :src="avatar" alt="Player avatar" class="h-full w-full object-cover" />
      </div>
      <div>
        <p class="text-xs uppercase tracking-[0.35em] text-fog/60">Player</p>
        <h3 class="text-lg font-semibold">{{ name || "Unknown" }}</h3>
        <p class="text-xs text-fog/50">{{ steamId }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  steamId: String,
  avatar: String,
});
</script>
