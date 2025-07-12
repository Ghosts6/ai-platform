// Proxy README.md requests to the root README.md file
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/README.md',
    createProxyMiddleware({
      target: 'http://localhost:8000', // Django dev server
      changeOrigin: true,
      pathRewrite: { '^/README.md': '/README.md' },
    })
  );
};
