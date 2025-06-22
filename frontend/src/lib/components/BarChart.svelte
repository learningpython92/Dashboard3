<!-- src/lib/components/BarChart.svelte -->
<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  /**
   * chartData is an array of objects from your API, e.g.,
   * [{ label: 'Sales', value: 80 }, { label: 'HR', value: 45 }]
   */
  export let chartData = [];
  export let kpiName = "Value";

  let canvasElement;
  let chart;

  // This function formats our API data for Chart.js
  function formatChartData(data) {
    const labels = data.map(d => d.label);
    const values = data.map(d => d.value);

    return {
      labels,
      datasets: [
        {
          label: kpiName,
          data: values,
          backgroundColor: 'rgba(136, 132, 216, 0.6)', // A nice purple, similar to the React reference
          borderColor: 'rgba(136, 132, 216, 1)',
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    };
  }

  // onMount runs once the component is added to the page.
  onMount(() => {
    const ctx = canvasElement.getContext('2d');
    chart = new Chart(ctx, {
      type: 'bar', // The only major change is the chart type
      data: formatChartData(chartData),
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            backgroundColor: 'rgba(31, 41, 55, 0.9)',
            titleColor: '#f3f4f6',
            bodyColor: '#d1d5db',
            borderColor: '#4b5563',
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            ticks: { color: '#9ca3af' },
            grid: { display: false }, // Bar charts often look cleaner without vertical grid lines
          },
          y: {
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(75, 85, 99, 0.3)' },
            beginAtZero: true, // It's usually best for bar charts to start at zero
          },
        },
      },
    });
  });

  // This reactive statement automatically updates the chart when the data changes.
  $: if (chart && chartData) {
    chart.data = formatChartData(chartData);
    chart.update('none');
  }
</script>

<div class="relative h-64 w-full">
  <canvas bind:this={canvasElement}></canvas>
</div>
