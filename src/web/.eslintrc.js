module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/recommended",
    "eslint:recommended",
    "plugin:prettier-vue/recommended",
    "plugin:jsdoc/recommended",
    "prettier/vue",
  ],
  ignorePatterns: ["*.min.js", "*.ts"],
  parserOptions: {
    parser: "@babel/eslint-parser",
  },
  plugins: ["jsdoc"],
  rules: {
    "no-console": process.env.ENV === "production" ? "error" : "off",
    "no-debugger": process.env.ENV === "production" ? "error" : "off",
  },
  settings: {
    jsdoc: {
      mode: "typescript",
    },
  },
};
