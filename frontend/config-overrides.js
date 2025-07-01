const path = require('path');
const { override } = require('customize-cra');

module.exports = {
  webpack: function (config, env) {
    if (env === 'production') {
      // Output settings for JavaScript
      config.output.filename = 'js/main.js';
      config.output.chunkFilename = 'js/[name].chunk.js';
      config.output.path = path.resolve(__dirname, 'dist');

      // CSS output settings
      config.plugins.forEach(plugin => {
        if (plugin.constructor.name === 'MiniCssExtractPlugin') {
          plugin.options.filename = 'css/main.css';
          plugin.options.chunkFilename = 'css/[name].chunk.css';
        }
      });
    }
    return config;
  },
  paths: function (paths, env) {
    paths.appBuild = path.resolve(__dirname, 'dist');
    return paths;
  },
};
