<template>
  <div class="glass rounded-2xl p-6">
    <h3 class="text-lg font-semibold">Key Metrics</h3>
    <div class="mt-4 overflow-x-auto">
      <table class="w-full text-left text-sm">
        <thead class="text-fog/60">
          <tr>
            <th class="py-2">Metric</th>
            <th class="py-2">Player A</th>
            <th class="py-2">Player B</th>
            <th class="py-2">Winner</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="stat in stats"
            :key="stat.key"
            class="border-t border-fog/10"
          >
            <td class="py-3">{{ stat.label }}</td>
            <td class="py-3">{{ formatValue(stat.playerAValue, stat.unit) }}</td>
            <td class="py-3">{{ formatValue(stat.playerBValue, stat.unit) }}</td>
            <td class="py-3">
              <span
                class="rounded-full px-3 py-1 text-xs"
                :class="{
                  'bg-ember text-ink': stat.winner === 'playerA',
                  'bg-tide text-ink': stat.winner === 'playerB',
                  'bg-fog/10 text-fog/60': stat.winner === 'tie'
                }"
              >
                {{ winnerLabel(stat.winner) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: {
    type: Array,
    default: () => [],
  },
});

function formatValue(value, unit) {
  if (value === null || value === undefined) {
    return "-";
  }
  return unit ? `${value}${unit}` : value;
}

function winnerLabel(winner) {
  if (winner === "playerA") return "Player A";
  if (winner === "playerB") return "Player B";
  return "Tie";
}
</script>
