import eslint from "@eslint/js";
import prettier from "eslint-config-prettier";
import vue from "eslint-plugin-vue";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  // standard configs
  eslint.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  tseslint.configs.eslintRecommended,
  ...tseslint.configs.stylisticTypeChecked,
  {
    extends: [vue.configs["flat/recommended"]]
  },
  prettier,
  // additional rules we want to use
  {
    rules: {
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
          order: ["script:not([setup])", "script[setup]", "template"]
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

      "vue/html-self-closing": [
        "error",
        {
          html: {
            void: "any"
          }
        }
      ],

      "vue/no-boolean-default": ["error", "no-default"],
      "vue/no-ref-object-reactivity-loss": ["warn"],

      "vue/no-required-prop-with-default": [
        "error",
        {
          autofix: true
        }
      ],

      "vue/no-restricted-block": [
        "error",
        {
          element: "style",
          message:
            "Do not use <style> block in this project.\n We use TailwindCSS instead; look here: https://tailwindcss.com/docs/utility-first"
        },
        {
          element: "route",
          message:
            "Do not use <route> block in this project.\n Use definePage() instead; look here: https://uvr.esm.is/guide/extending-routes.html#definepage"
        }
      ],
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
      globals: globals.browser,
      parserOptions: {
        parser: "@typescript-eslint/parser",
        project: "tsconfig.app.json",
        extraFileExtensions: [".vue"],
        tsconfigRootDir: import.meta.dirname
      }
    }
  },
  {
    files: ["src/views/**/*.vue"],
    rules: {
      "vue/multi-word-component-names": ["off"]
    }
  },
  { ignores: ["dist/**/*.*", "*.js.timestamp"] },
  {
    plugins: {
      vue
    }
  }
);
