// frontend/svelte.config.js

// CORRECTED: We import adapter-node instead of adapter-auto.
// This specifically tells SvelteKit to build a Node.js server,
// which is exactly what Render needs to run your application.
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://kit.svelte.dev/docs/integrations#preprocessors
    // for more information about preprocessors
    preprocess: vitePreprocess(),

    kit: {
        // CORRECTED: We explicitly set the adapter to adapter-node.
        // This will create the `build/index.js` file that Render's start command expects.
        adapter: adapter()
    }
};

export default config;
