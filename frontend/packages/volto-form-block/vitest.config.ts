import { defineConfig } from 'vitest/config';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  resolve: {
    alias: {
      // Mirror tsconfig's `@plone/volto-form-block/*` -> `./src/*` path so unit
      // tests can resolve the package's self-referential imports.
      '@plone/volto-form-block': fileURLToPath(
        new URL('./src', import.meta.url),
      ),
    },
  },
});
