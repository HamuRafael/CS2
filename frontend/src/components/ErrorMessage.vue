<template>
  <div class="rounded-xl border border-ember/40 bg-ember/10 px-4 py-3 text-sm text-ember">
    {{ message }}
  </div>
</template>

<script setup>
defineProps({
  message: String,
});
</script>
