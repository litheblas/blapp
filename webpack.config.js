const path = require('path')

const PROJECT_ROOT = path.resolve(__dirname)
const WEBCLIENT_ROOT = path.resolve(PROJECT_ROOT, 'blapp', 'webclient')

module.exports = {
  entry: path.resolve(WEBCLIENT_ROOT, 'src', 'index.tsx'),
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
    ],
  },
  resolve: {
    extensions: [ '.tsx', '.ts', '.js' ],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(WEBCLIENT_ROOT, 'static'),
  },
}
