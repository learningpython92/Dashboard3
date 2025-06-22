// src/lib/api.js

// Using import.meta.env is the correct SvelteKit/Vite way to access environment variables.
// This will read the VITE_API_BASE_URL you set in your Vercel project settings.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function buildQueryParams(params) {
  const query = new URLSearchParams();
  for (const key in params) {
    if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
      query.append(key, params[key]);
    }
  }
  return query.toString();
}

/**
 * MODIFIED: Now accepts `fetch` as an argument.
 * This allows the function to use the special, server-aware `fetch` from SvelteKit's `load` function.
 */
export async function getDashboardData(filters, fetch) {
  const queryString = buildQueryParams(filters);
  const [kpiRes, insightsRes] = await Promise.all([
    fetch(`${API_BASE_URL}/kpis/averages/?${queryString}`),
    fetch(`${API_BASE_URL}/insights/deep-dive/?${queryString}`)
  ]);

  if (!kpiRes.ok || !insightsRes.ok) {
    throw new Error('Failed to fetch dashboard data from API.');
  }
  return {
    kpiData: await kpiRes.json(),
    insightData: await insightsRes.json(),
  };
}

/**
 * MODIFIED: Now accepts `fetch` as an argument.
 */
export async function getDrilldownData(kpiKey, filters, fetch) {
  const drilldownFilters = {
    business_group: filters.business_group,
    function: filters.function,
  };
  const queryString = buildQueryParams(drilldownFilters);
  const response = await fetch(`${API_BASE_URL}/kpis/drilldown/${kpiKey}?${queryString}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch drilldown data for ${kpiKey} from API.`);
  }
  return response.json();
}

/**
 * MODIFIED: Now accepts `fetch` as an argument.
 */
export async function getFilterOptions(fetch) {
  const [bizGroupsRes, functionsRes] = await Promise.all([
    fetch(`${API_BASE_URL}/filters/business-groups`),
    fetch(`${API_BASE_URL}/filters/functions`)
  ]);
  if (!bizGroupsRes.ok || !functionsRes.ok) {
    throw new Error('Failed to fetch filter options from API.');
  }
  return {
    businessGroups: await bizGroupsRes.json(),
    functions: await functionsRes.json(),
  };
}

/**
 * MODIFIED: Now accepts `fetch` as an argument.
 */
export async function getHeadcountData(fetch) {
  const response = await fetch(`${API_BASE_URL}/summaries/`);
  if (!response.ok) {
    throw new Error('Failed to fetch headcount data from API.');
  }
  return response.json();
}
