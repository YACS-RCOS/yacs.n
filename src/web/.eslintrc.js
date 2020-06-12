module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ["plugin:vue/essential", "eslint:recommended", "prettier"],
  ignorePatterns: ["*.min.js"],
  parserOptions: {
    parser: "babel-eslint",
  },
  rules: {
    "no-console": process.env.ENV === "production" ? "error" : "off",
    "no-debugger": process.env.ENV === "production" ? "error" : "off",
  },
};
