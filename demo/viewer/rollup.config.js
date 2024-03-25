import { nodeResolve } from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
//import { terser } from '@rollup/plugin-terser';

export default {
  input: {
    viewer: "viewer.js",
  },
  output: {
    dir: "build",
    format: "esm",
    //format: 'cjs'
    //sourcemap: true,
  },
  plugins: [
    nodeResolve(), // resolve modules from node_modules
    commonjs(), // convert CommonJS modules to ES6
    //terser(), // minify the output
  ],
};
