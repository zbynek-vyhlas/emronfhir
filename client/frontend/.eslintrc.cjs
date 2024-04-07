/* eslint-env node */
// require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],
  parserOptions: {
    ecmaVersion: "latest",
    // "sourceType": "module"
  },
  env: {
    browser: true,
    es6: true,
  },
  plugins: ["vue"],
  rules: {
    // Your rules here
  },
};
