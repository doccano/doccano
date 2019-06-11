const fs = require('fs');
const path = require('path');
const process = require('process');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const { ContextReplacementPlugin } = require('webpack');
const hljsLanguages = require('./components/hljsLanguages');

const devMode = process.env.DEBUG !== 'False';
const hotReload = process.env.HOT_RELOAD === '1';
const webpackHost = process.env.WEBPACK_HOST || '127.0.0.1';
const webpackPort = process.env.WEBPACK_PORT ? parseInt(process.env.WEBPACK_PORT, 10) : 8080;
const pollMillis = process.env.WEBPACK_POLL_MILLIS ? parseInt(process.env.WEBPACK_POLL_MILLIS, 10) : false;
const noSourceMap = process.env.SOURCE_MAP === 'False';

const pagesRoot = path.join(__dirname, 'pages');
const entryPoints = {};
fs.readdirSync(pagesRoot).forEach((scriptName) => {
    const bundleName = path.parse(scriptName).name;
    const scriptPath = path.join(pagesRoot, scriptName)
    entryPoints[bundleName] = scriptPath;
});

module.exports = {
    mode: devMode ? 'development' : 'production',
    entry: entryPoints,
    output: {
        publicPath: hotReload ? `http://127.0.0.1:${webpackPort}/` : '',
        path: path.join(__dirname, 'bundle'),
        filename: '[name].js'
    },
    devtool: noSourceMap ? false : (devMode ? 'cheap-eval-source-map' : 'source-map'),
    devServer: {
        port: webpackPort,
        host: webpackHost,
        hot: true,
        quiet: false,
        headers: { 'Access-Control-Allow-Origin': '*' }
    },
    watchOptions: {
        poll: pollMillis,
    },
    module: {
        rules: [
            {
                test: /\.pug$/,
                loader: 'pug-plain-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            }
        ]
    },
    plugins: [
        new ContextReplacementPlugin(
            /highlight\.js\/lib\/languages$/,
            new RegExp(`^./(${hljsLanguages.join('|')})$`)
        ),
        new BundleTracker({ filename: './webpack-stats.json' }),
        new VueLoaderPlugin()
    ],
    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            vue$: 'vue/dist/vue.esm.js',
        },
    },
}