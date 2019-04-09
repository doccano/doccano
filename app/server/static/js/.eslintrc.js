module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true,
  },
  parserOptions: {
    parser: "babel-eslint",
  },
  extends: [
    "airbnb-base",
  ],
  rules: {
    "no-param-reassign": "off",
    "no-plusplus": "off",
    "object-shorthand": "off",
    "prefer-destructuring": "off",
    "prefer-template": "off",
  },
};
// https://travishorn.com/setting-up-eslint-on-vs-code-with-airbnb-javascript-style-guide-6eb78a535ba6