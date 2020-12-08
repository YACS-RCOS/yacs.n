const path = require("path");
const MomentLocalesPlugin = require("moment-locales-webpack-plugin");
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = {
  chainWebpack(config) {
    config.plugins.delete('prefetch');
    config.plugin('CompressionPlugin').use(CompressionPlugin);
  },
  devServer: {
    disableHostCheck: true,
    proxy: {
      "/api": {
        target: process.env.YACS_API_HOST || "http://localhost:5000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  configureWebpack: {
    plugins: [new MomentLocalesPlugin()],
    devtool:
      process.env.VUE_APP_ENVIRONMENT == "development" ? "source-map" : "none",
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "@/assets/_bootstrap_helpers.scss";`,
      },
    },
  },
};
