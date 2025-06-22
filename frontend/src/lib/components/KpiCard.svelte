<!-- src/lib/components/KpiCard.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';

  /**
   * Props for the KPI Card.
   * `label` is the name of the KPI (e.g., "Avg. Time to Fill").
   * `value` is the number or string to display.
   */
  export let label = '';
  export let value = '—';

  const dispatch = createEventDispatcher();

  function handleClick() {
    // This sends a 'kpiClick' event up to the parent component.
    // The parent will listen for this event to switch to the drilldown view.
    dispatch('kpiClick', { label });
  }
</script>

<!--
  This div uses the exact same styling as the KpiCard in the React reference.
  The on:click directive calls our handleClick function.
  The cursor-pointer and transition classes make it feel interactive.
-->
<div
  on:click={handleClick}
  class="bg-gray-800/60 p-4 rounded-lg shadow-md h-24 cursor-pointer hover:bg-gray-700/80 transition-colors flex flex-col justify-between"
  role="button"
  tabindex="0"
  on:keydown={(e) => e.key === 'Enter' && handleClick()}
>
  <h4 class="text-sm font-medium text-gray-400">{label}</h4>
  <p class="text-2xl font-bold text-white">{value}</p>
</div>
