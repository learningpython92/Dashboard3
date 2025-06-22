<!-- src/lib/components/LineChart.svelte -->
<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  /**
   * chartData is an array of objects from your API, e.g.,
   * [{ label: 'Jan', value: 50 }, { label: 'Feb', value: 65 }]
   */
  export let chartData = [];
  export let kpiName = "Value"; // To label the line in the tooltip

  let canvasElement;
  let chart;

  // This function takes our API data and formats it for Chart.js
  function formatChartData(data) {
    // Uses the `label` key from your API response for the X-axis
    const labels = data.map(d => d.label); 
    // Uses the `value` key for the Y-axis data points
    const values = data.map(d => d.value);

    return {
      labels,
      datasets: [
        {
          label: kpiName,
          data: values,
          borderColor: '#3b82f6', // A bright blue for visibility
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4, // This creates a smooth, curved line
          pointBackgroundColor: '#3b82f6',
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    };
  }
  
  // onMount runs once the component is added to the page.
  // This is where we create the chart.
  onMount(() => {
    const ctx = canvasElement.getContext('2d');
    chart = new Chart(ctx, {
      type: 'line',
      data: formatChartData(chartData),
      options: {
        responsive: true,
        maintainAspectRatio: false, // Allows chart to fill the container's height
        plugins: {
          legend: {
            display: false, // The chart is simple, so we hide the legend.
          },
          tooltip: {
            backgroundColor: 'rgba(31, 41, 55, 0.9)', // Dark background for tooltip
            titleColor: '#f3f4f6',
            bodyColor: '#d1d5db',
            borderColor: '#4b5563',
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            ticks: { color: '#9ca3af' }, // Style for X-axis labels
            grid: { color: 'rgba(75, 85, 99, 0.3)' }, // Style for X-axis grid lines
          },
          y: {
            ticks: { color: '#9ca3af' }, // Style for Y-axis labels
            grid: { color: 'rgba(75, 85, 99, 0.3)' }, // Style for Y-axis grid lines
            beginAtZero: false, // Lets the Y-axis start from a value other than 0 for better visibility
          },
        },
      },
    });
  });

  // This is a Svelte "reactive statement".
  // It automatically re-runs whenever the `chartData` prop changes.
  $: if (chart && chartData) {
    chart.data = formatChartData(chartData);
    chart.update('none'); // 'none' prevents animations on update
  }
</script>

<!-- 
  We need a container to give the canvas a responsive size.
  The canvas element itself is bound to our `canvasElement` variable.
-->
<div class="relative h-64 w-full">
  <canvas bind:this={canvasElement}></canvas>
</div>
