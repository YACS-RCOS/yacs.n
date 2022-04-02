module.exports = {
    ci: {
        collect: {
            url: ['https://localhost'],
            settings: {
                chromeFlags: ['--ignore-certificate-errors', '--show-paint-rects', '--headless'],
                // --- comment the formFactor and screenEmulation to test for mobile ---
                formFactor: 'desktop',      
                screenEmulation: {
                    mobile: false,
                    width: 1920,
                    height: 1080,
                    deviceScaleFactor: 1,
                    disabled: false,
                }
            }
        },
        assert:{
            assertions: {
                'categories:performance': ['warn', { 'minScore': 0.8 }],
                'categories:accessibility': ['warn', { 'minScore': 0.8 }],
                'categories:best-practices': ['error', { 'minScore': 1.0 }],
                'categories:seo': ['warn', { 'minScore': 1.0 }],
            }
        },
        upload: {
            target: 'temporary-public-storage'
        }
    }
}