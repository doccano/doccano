const process = require('process');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const devMode = process.env.DEBUG !== 'False';
const hotReload = process.env.HOT_RELOAD === '1';

module.exports = {
    mode: devMode ? 'development' : 'production',
    entry: {
        'index': './static/js/entrypoints/index.js',
        'sequence_labeling': './static/js/entrypoints/annotation/sequence_labeling.js',
        'document_classification': './static/js/entrypoints/annotation/document_classification.js',
        'seq2seq': './static/js/entrypoints/annotation/seq2seq.js',
        'projects': './static/js/entrypoints/admin/projects.js',
        'stats': './static/js/entrypoints/admin/stats.js',
        'label': './static/js/entrypoints/admin/label.js',
        'guideline': './static/js/entrypoints/admin/guideline.js',
        'demo_text_classification': './static/js/entrypoints/demo/demo_text_classification.js',
        'demo_named_entity': './static/js/entrypoints/demo/demo_named_entity.js',
        'demo_translation': './static/js/entrypoints/demo/demo_translation.js',
        'upload_seq2seq': './static/js/entrypoints/admin/upload_seq2seq.js',
        'upload_sequence_labeling': './static/js/entrypoints/admin/upload_sequence_labeling.js',
        'upload_text_classification': './static/js/entrypoints/admin/upload_text_classification.js',
        'download_seq2seq': './static/js/entrypoints/admin/download_seq2seq.js',
        'download_sequence_labeling': './static/js/entrypoints/admin/download_sequence_labeling.js',
        'download_text_classification': './static/js/entrypoints/admin/download_text_classification.js',
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