const VueLoaderPlugin = require('vue-loader/lib/plugin')

    module.exports = {
    module: {
	rules: [
		// ... other rules
{
    test: /\.vue$/,
    loader: 'vue-loader'
}
    ]
    },
    plugins: [
	      // make sure to include the plugin!
	      new VueLoaderPlugin()
	      ],
    resolve: {
	extensions: ['.js', '.vue'],
	alias: {
	    vue$: 'vue/dist/vue.esm.js', //webpack使う場合はこっちを指定する https://jp.vuejs.org/v2/guide/installation.html#%E7%94%A8%E8%AA%9E
	},
    },
}