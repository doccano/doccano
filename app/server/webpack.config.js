const process = require('process');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const devMode = process.env.DEBUG !== 'False';
const hotReload = process.env.HOT_RELOAD === '1';
const webpackHost = process.env.WEBPACK_HOST || '127.0.0.1';
const webpackPort = process.env.WEBPACK_PORT ? parseInt(process.env.WEBPACK_PORT, 10) : 8080;
const pollMillis = process.env.WEBPACK_POLL_MILLIS ? parseInt(process.env.WEBPACK_POLL_MILLIS, 10) : false;

module.exports = {
    mode: devMode ? 'development' : 'production',
    entry: {
        'index': './static/js/index.js',
        'sequence_labeling': './static/js/sequence_labeling.js',
        'document_classification': './static/js/document_classification.js',
        'seq2seq': './static/js/seq2seq.js',
        'projects': './static/js/projects.js',
        'stats': './static/js/stats.js',
        'label': './static/js/label.js',
        'guideline': './static/js/guideline.js',
        'demo_text_classification': './static/js/demo/demo_text_classification.js',
        'demo_named_entity': './static/js/demo/demo_named_entity.js',
        'demo_translation': './static/js/demo/demo_translation.js',
        'upload_seq2seq': './static/js/upload_seq2seq.js',
        'upload_sequence_labeling': './static/js/upload_sequence_labeling.js',
        'upload_text_classification': './static/js/upload_text_classification.js',
        'download_seq2seq': './static/js/download_seq2seq.js',
        'download_sequence_labeling': './static/js/download_sequence_labeling.js',
        'download_text_classification': './static/js/download_text_classification.js',
    },
    output: {
        publicPath: hotReload ? `http://127.0.0.1:${webpackPort}/` : '',
        path: __dirname + '/static/bundle',
        filename: '[name].js'
    },
    devtool: devMode ? 'cheap-eval-source-map' : 'source-map',
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