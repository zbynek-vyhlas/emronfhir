const basicRule = [(v) => !!v || "This field is required"];

const emailRules = [
  ...basicRule,
  (v) => /.+@.+\..+/.test(v) || "Email must be valid",
];

const passwordRules = [
  ...basicRule,
  (v) => (!!v && v.length >= 8) || "Password must be at least 8 characters",
];

const password2Rules = (password1, password2) => [
  ...passwordRules,
  () => password1 === password2 || "Passwords must match",
];

export { basicRule, emailRules, passwordRules, password2Rules };
