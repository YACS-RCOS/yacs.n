const path = require("path");
const MomentLocalesPlugin = require("moment-locales-webpack-plugin");

module.exports = {
  devServer: {
    disableHostCheck: true,
    proxy: {
      "/api": {
        target: process.env.YACS_API_HOSTNAME || "http://localhost:5000",
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
};
