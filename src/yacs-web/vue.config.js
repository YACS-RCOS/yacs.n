const MomentLocalesPlugin = require('moment-locales-webpack-plugin');

module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true
            }
        },
    },
    configureWebpack: {
        plugins: [
            new MomentLocalesPlugin()
        ],
        devtool: process.env.VUE_APP_ENVIRONMENT == 'development' ? 'source-map' : 'none'
    }
}