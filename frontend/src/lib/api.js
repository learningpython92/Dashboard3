// src/lib/api.js

// This constant holds the base URL for your FastAPI backend.
const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * A helper function to safely build URL query strings from a filters object.
 * It ignores null, undefined, or empty string values.
 * @param {object} params - The key-value pairs for the query string.
 * @returns {string} - A URL-encoded query string.
 */
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
 * Fetches all necessary data for the main dashboard view.
 * @param {object} filters - An object containing { business_group, function, start_date, end_date }.
 * @returns {Promise<{kpiData: object, insightData: object}>} - A promise that resolves to the combined dashboard data.
 */
export async function getDashboardData(filters) {
  const queryString = buildQueryParams(filters);

  // We fetch both endpoints in parallel for better performance.
  const [kpiRes, insightsRes] = await Promise.all([
    fetch(`${API_BASE_URL}/kpis/averages/?${queryString}`),
    fetch(`${API_BASE_URL}/insights/deep-dive/?${queryString}`)
  ]);

  if (!kpiRes.ok || !insightsRes.ok) {
    throw new Error('Failed to fetch dashboard data.');
  }

  const kpiData = await kpiRes.json();
  const insightData = await insightsRes.json();

  return { kpiData, insightData };
}


/**
 * Fetches the data needed for the KPI drilldown view.
 * @param {string} kpiKey - The key for the KPI (e.g., 'time_to_fill').
 * @param {object} filters - An object containing { business_group, function }. Note: dates are intentionally ignored per requirements.
 * @returns {Promise<object>} - A promise that resolves to the drilldown data.
 */
export async function getDrilldownData(kpiKey, filters) {
  // Only use business_group and function for the drilldown query.
  const drilldownFilters = {
    business_group: filters.business_group,
    function: filters.function,
  };
  const queryString = buildQueryParams(drilldownFilters);

  const response = await fetch(`${API_BASE_URL}/kpis/drilldown/${kpiKey}?${queryString}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch drilldown data for ${kpiKey}.`);
  }

  return response.json();
}

/**
 * Fetches the unique lists of business groups and functions for the filter controls.
 * @returns {Promise<{businessGroups: string[], functions: string[]}>} - A promise that resolves to the filter options.
 */
export async function getFilterOptions() {
  const [bizGroupsRes, functionsRes] = await Promise.all([
    fetch(`${API_BASE_URL}/filters/business-groups`),
    // CORRECTED: Was using a non-existent "API_MOCK_BASE_URL"
    fetch(`${API_BASE_URL}/filters/functions`)
  ]);

  if (!bizGroupsRes.ok || !functionsRes.ok) {
    throw new Error('Failed to fetch filter options.');
  }

  const businessGroups = await bizGroupsRes.json();
  const functions = await functionsRes.json();

  return { businessGroups, functions };
}

/**
 * Fetches the complete headcount summary data.
 * @returns {Promise<Array>} - A promise that resolves to the array of headcount records.
 */
export async function getHeadcountData() {
  const response = await fetch(`${API_BASE_URL}/summaries/`); 
  if (!response.ok) {
    throw new Error('Failed to fetch headcount data.');
  }
  return response.json();
}
