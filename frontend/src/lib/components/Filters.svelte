<!-- src/lib/components/Filters.svelte -->

<script>
  /**
   * Props for the Filters component.
   * `export let` is how you declare props in Svelte.
   */
  export let businessUnits = [];
  export let functions = [];
  
  // `bind:value` in Svelte provides two-way data binding.
  export let selectedBU;
  export let selectedFunction;
  export let dateRange;
</script>

<div class="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700 p-6 mb-8">
  <div class="grid grid-cols-1 lg:grid-cols-10 gap-x-6 gap-y-4 items-center">

    <!-- Business Unit Buttons -->
    <div class="lg:col-span-5 flex gap-2 overflow-x-auto pb-2">
      {#each businessUnits as unit}
        <button
          on:click={() => (selectedBU = unit)}
          class="px-4 py-2 text-sm rounded-lg font-semibold transition whitespace-nowrap {selectedBU === unit
            ? 'bg-blue-600 text-white shadow-lg scale-105'
            : 'bg-gray-700/50 text-gray-300 hover:bg-gray-700'}"
        >
          {unit}
        </button>
      {/each}
    </div>

    <!-- Function Dropdown -->
    <div class="lg:col-span-2">
      <select
        bind:value={selectedFunction}
        class="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:outline-none"
      >
        {#each functions as func}
          <option value={func} class="bg-gray-800 text-white">{func}</option>
        {/each}
      </select>
    </div>

    <!-- Date Range Inputs -->
    <div class="lg:col-span-3 flex gap-2 items-center">
      <input
        type="date"
        bind:value={dateRange.start}
        class="w-full px-2 py-2 text-sm bg-gray-700/50 border border-gray-600 rounded-lg text-white"
      />
      <span class="text-gray-500">-</span>
      <input
        type="date"
        bind:value={dateRange.end}
        class="w-full px-2 py-2 text-sm bg-gray-700/50 border border-gray-600 rounded-lg text-white"
      />
    </div>
  </div>
</div>
