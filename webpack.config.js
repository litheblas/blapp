const path = require('path')

const PROJECT_ROOT = path.resolve(__dirname)
const FRONTEND_ROOT = path.resolve(PROJECT_ROOT, 'blapp', 'frontend')

module.exports = {
  entry: {
    // Add more bundles here.
    base: path.resolve(FRONTEND_ROOT, 'src', 'base', 'index.tsx'),
    commerce: path.resolve(FRONTEND_ROOT, 'src', 'commerce', 'index.tsx'),
    style: path.resolve(FRONTEND_ROOT, 'src', 'style', 'index.scss'),
  },
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(scss)$/,
        use: [
          {
            loader: 'style-loader',
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: () => [
                require('precss'),
                require('autoprefixer'),
              ]
            }
          },
          {
            loader: 'sass-loader',
          },
        ],
      },

    ],
  },
  resolve: {
    extensions: [ '.tsx', '.ts', '.js', '.scss' ],
    alias: {
      blapp: path.resolve(FRONTEND_ROOT, 'src'),
    },
  },
  output: {
    filename: '[name]/bundle.js',
    path: path.resolve(FRONTEND_ROOT, 'static'),
  },
  performance: {
    // Don't whine until we hit 5 MiB
    maxAssetSize: 5242880,
    maxEntrypointSize: 5242880,
  }
}
