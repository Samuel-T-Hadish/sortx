/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./sortx/pages/**/*.py", // scans all Python files in the pages directory
    "./sortx/components/**/*.py", // scans all Python files in the components directory
    "./sortx/app/**/*.py", // scans all Python files in the app directory
    "./sortx/app.py", // scans all Python files in the lib directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
