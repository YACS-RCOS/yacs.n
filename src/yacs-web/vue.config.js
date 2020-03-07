const MomentLocalesPlugin = require('moment-locales-webpack-plugin');

process.env

module.exports = {
    configureWebpack: {
        plugins: [
            new MomentLocalesPlugin()
        ],
        devtool: process.env.VUE_APP_ENVIRONMENT == 'development' ? 'source-map' : 'none'
    }
}