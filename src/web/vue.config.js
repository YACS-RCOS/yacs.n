const path = require("path");
const MomentLocalesPlugin = require("moment-locales-webpack-plugin");
const CompressionPlugin = require("compression-webpack-plugin");

module.exports = {
  chainWebpack(config) {
    if (process.env.NODE_ENV === "production") {
      config.plugins.delete("prefetch");
      config.plugin("CompressionPlugin").use(CompressionPlugin);
    }
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
    devtool: "source-map",
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
    output: {
      devtoolModuleFilenameTemplate: (info) => {
        const isGeneratedDuplicate =
          info.resourcePath.match(/\.vue$/) && info.allLoaders;
        if (isGeneratedDuplicate) {
          return `webpack-generated:///${info.resourcePath}?${info.hash}`;
        }
        return `webpack:///${path.normalize(info.resourcePath)}`;
      },
      devtoolFallbackModuleFilenameTemplate:
        "webpack:///[resource-path]?[hash]",
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
