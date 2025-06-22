<!-- src/lib/components/InsightCard.svelte -->
<script>
  /**
   * Props for the Insight Card.
   * `title` is the heading for the insight (e.g., "Key Observation").
   * `description` is the main text content of the insight.
   */
  export let title = 'Insight';
  export let description = 'No description available.';

  // A reactive variable to check if the insight is a warning or API error.
  // `$` makes this variable automatically recalculate whenever `description` changes.
  $: isWarning = description.startsWith('⚠️');
</script>

<!--
  The static and dynamic classes have been combined into a single `class` attribute
  using a ternary operator to fix the compiler error.
-->
<div
  class="bg-gray-800/60 p-6 rounded-lg shadow-md {isWarning ? 'border border-red-700/50' : ''}"
>
  <!-- The title color also changes based on whether it's a warning. -->
  <h3
    class="font-semibold mb-2 {isWarning ? 'text-red-400' : 'text-blue-400'}"
  >
    {title}
  </h3>
  <p class="text-gray-400 text-sm">{description.replace(/^- /, '')}</p>
</div>
