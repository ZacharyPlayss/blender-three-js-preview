import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'node:fs/promises';

export default defineConfig({
    build: {
        //OutDir set to root so we can compress bundled version to the release.
        outDir: '../webserver',
        emptyOutDir: true,
        rollupOptions: {
            output: {
                entryFileNames: 'scripts/[name].js',
                chunkFileNames: 'scripts/[name].js',
                assetFileNames: (chunkInfo) => {
                    if (chunkInfo.name?.endsWith('.css')) {
                        return 'styles/[name][extname]';
                    }
                    return 'assets/[name][extname]';
                },
            },
        },
    },
    plugins: [
        {
            name: 'create-empty-models-dir',
            async closeBundle() {
                const modelsDir = resolve(process.cwd(), 'webserver/assets/models');
                try {
                    await fs.mkdir(modelsDir, { recursive: true });
                    console.log('\x1b[32m%s\x1b[0m', '  ✓ created empty assets/models directory');
                } catch (err) {
                    console.error('Could not create models directory:', err);
                }
            },
        },
    ],
});