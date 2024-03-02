import eslint from "@eslint/js";
import prettier from "eslint-config-prettier";
import tseslint from "typescript-eslint";

// @ts-expect-error Vue Eslint plugin does not support TS yet
import vuelint from "eslint-plugin-vue";

/** @type {Record<string, import("typescript-eslint").configs.base.rules>} */
// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-assignment
const vuelint_rules = Object.fromEntries(
  // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
  Object.entries(vuelint.configs).map(([k, v]) => [k, v.rules])
);

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  tseslint.configs.eslintRecommended,
  ...tseslint.configs.stylisticTypeChecked,
  {
    rules: {
      ...vuelint_rules["vue3-essential"],
      ...vuelint_rules["vue3-strongly-recommended"],
      ...vuelint_rules["vue3-recommended"],

      "vue/block-lang": [
        "error",
        {
          script: {
            lang: "ts"
          }
        }
      ],

      "vue/block-order": [
        "error",
        {
          order: ["script[setup]", "script:not([setup])", "template"]
        }
      ],

      "vue/component-api-style": ["error", ["script-setup"]],
      "vue/define-emits-declaration": ["error", "type-literal"],

      "vue/define-macros-order": [
        "error",
        {
          order: ["defineOptions", "defineModel", "defineProps", "defineEmits", "defineSlots"],
          defineExposeLast: true
        }
      ],

      "vue/define-props-declaration": ["error", "type-based"],
      "vue/no-boolean-default": ["error", "no-default"],
      "vue/no-ref-object-reactivity-loss": ["warn"],

      "vue/no-required-prop-with-default": [
        "error",
        {
          autofix: true
        }
      ],

      "vue/no-restricted-block": ["error", "style"],
      "vue/no-useless-mustaches": ["error"],
      "vue/prefer-separate-static-class": ["error"],
      "vue/require-typed-object-prop": ["error"],
      "vue/require-typed-ref": ["error"],
      "vue/valid-define-options": ["error"]
    }
  },
  {
    files: ["*.{js,ts}"],
    languageOptions: {
      parserOptions: {
        project: "tsconfig.node.json",
        tsconfigRootDir: import.meta.dirname
      }
    }
  },
  {
    files: ["src/**/*.{js,ts,vue}"],
    languageOptions: {
      parser: await import("vue-eslint-parser"),
      parserOptions: {
        parser: "@typescript-eslint/parser",
        project: "tsconfig.app.json",
        extraFileExtensions: [".vue"],
        tsconfigRootDir: import.meta.dirname
      }
    }
  },
  {
    plugins: {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      vue: vuelint
    }
  },
  prettier
);
