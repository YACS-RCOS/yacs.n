module.exports = {
    ci: {
        collect: {
            url: ['https://localhost']
        },
        assert:{
            assertions: {
                'categories:performance': ['error', { 'minScore': 0.8 }],
                'categories:accessibility': ['error', { 'minScore': 0.8 }],
                'categories:best-practices': ['error', { 'minScore': 1.0 }],
                'categories:seo': ['error', { 'minScore': 1.0 }]
            }
        },
        upload: {
            target: 'temporary-public-storage'
        }
    }
}