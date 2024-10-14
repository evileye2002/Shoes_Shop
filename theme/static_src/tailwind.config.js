/**
 * Crispy Form TailwinCss fix
 * https://saashammer.com/blog/render-django-form-with-tailwind-css-style/#jit
 */
//#region Crispy Form TailwinCss fix
const Path = require("path");
const pySitePackages = process.env.Site_Packages || "";

// We can add current project paths here
const contentDefaults = [
  "../templates/**/*.html",
  "../../templates/**/*.html",
  "../../**/templates/**/*.html",
  "../../apps/**/forms.py",
  "../../**/node_modules/flowbite/**/*.js",
  "../../static/js/*.js",
  "../../**/static/js/*.js",
];

// We can add 3-party python packages here
let pyPackagesPaths = [];
if (pySitePackages) {
  pyPackagesPaths = [
    Path.join(pySitePackages, "./crispy_tailwind/**/*.html"),
    Path.join(pySitePackages, "./crispy_tailwind/**/*.py"),
    Path.join(pySitePackages, "./crispy_tailwind/**/*.js"),
  ];
}

const contentPaths = [...contentDefaults, ...pyPackagesPaths];
console.log(`tailwindcss will scan:`, contentPaths);
//#endregion

module.exports = {
  darkMode: ["selector"],
  content: contentPaths,
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
          950: "#172554",
        },
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    // require('@tailwindcss/forms'),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("flowbite/plugin")({
      charts: false,
      forms: true,
      tooltips: true,
    }),
  ],
};
