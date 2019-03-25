const process = require('process');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const devMode = process.env.DEBUG !== 'False';
const hotReload = process.env.HOT_RELOAD === '1';

module.exports = {
    mode: devMode ? 'development' : 'production',
    entry: {
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
        'upload': './static/js/upload.js',
        'dataset': './static/js/dataset.js',
    },
    output: {
        publicPath: hotReload ? 'http://localhost:8080/' : '',
        path: __dirname + '/static/bundle',
        filename: '[name].js'
    },
    devtool: devMode ? 'cheap-eval-source-map' : 'source-map',
    devServer: {
        hot: true,
        quiet: false,
        headers: { 'Access-Control-Allow-Origin': '*' }
    },
    module: {
        rules: [
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