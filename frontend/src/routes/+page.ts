// src/routes/+page.ts

// We import the API functions and a SvelteKit helper for creating errors.
import { getDashboardData, getFilterOptions, getHeadcountData } from '$lib/api.js';
import { error } from '@sveltejs/kit';

/**
 * This special `load` function runs on the server when a user first visits the page.
 * It receives a server-aware `fetch` from SvelteKit, which is crucial for Vercel.
 */
export async function load({ fetch }) {
  try {
    // Define the initial filters for the first page load.
    const initialFilters = {
      start_date: '2025-01-01',
      end_date: '2025-12-31',
    };
    
    // We call all our API functions in parallel, passing the special `fetch` to each one.
    // This is the key change that makes it work on Vercel.
    const [dashboardData, filterOptions, headcountData] = await Promise.all([
      getDashboardData(initialFilters, fetch),
      getFilterOptions(fetch),
      getHeadcountData(fetch)
    ]);

    // We return all the data we fetched.
    return {
      dashboardData,
      filterOptions,
      headcountData,
    };
  } catch (e) {
    // If any API call fails on the server, we throw a proper error.
    // This will show a real error page on Vercel instead of a generic 404.
    console.error("Vercel server-side load failed:", e);
    throw error(503, `The API is currently unavailable. Please try again later.`);
  }
}
