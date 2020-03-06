const MomentLocalesPlugin = require('moment-locales-webpack-plugin');

module.exports = {
    configureWebpack: {
        plugins: [
            new MomentLocalesPlugin()
        ],
        devtool: 'source-map'
    }
}