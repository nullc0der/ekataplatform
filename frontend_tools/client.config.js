var path = require('path');
var webpack = require('webpack');

var DIRS = require('./dirs.js');

var stylus = require('stylus');
var nib = require('nib');
var axis = require('axis');
var rupture = require('rupture');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ProgressPlugin = require('progress-bar-webpack-plugin');
var WebpackMd5Hash = require('webpack-md5-hash');
var ChunkManifestPlugin = require('chunk-manifest-webpack-plugin')
var OfflinePlugin = require('offline-plugin')
var BundleTracker = require('webpack-bundle-tracker')

const IS_PROD = process.env.NODE_ENV === "production";


const STYLUS_LOADER = (
	IS_PROD
		? {
			test: /\.styl$/,
			use: [
				{ loader: 'isomorphic-style-loader' },
				{
					loader: 'css-loader',
					options: { sourceMap: false }
				},
				{ loader: 'stylus-loader' }
			]
		}
		: {
			test: /\.styl$/,
			use: [
				{ loader: 'isomorphic-style-loader' },
				{
					loader: 'css-loader',
					options: {
						sourceMap: true,
						localIdentName: "[name]_[local]_[hash:base64:3]"
					}
				},
				{
					loader: 'stylus-loader'
				}
			]
		}
)


// const ISO_STYLUS_LOADER = (
// 	{
// 		test: /\.styl$/,
// 		use: [
// 			{ loader: 'isomorphic-style-loader' },
// 			{ loader: 'css-loader',
// 				options: {
// 					sourceMap: true,
// 					localIdentName: '[name]_[local]_[hash:base64:3]'
// 				}
// 			},
// 			{ loader: 'stylus-loader'}
// 		]
// 	}
// )

var config = {
	devtool: IS_PROD ? 'source-map' : 'eval',
	context: DIRS.SRC,
	cache: true,
	watchOptions: {
		ignored: /node_modules/
	},
	entry: {
		main: [
			DIRS.SRC_CLIENT + '/index.js'
		]
	},
	output: {
		path: DIRS.BUILD_PUBLIC,
		publicPath: '/statics/bundles/',
		chunkFilename: '[name].[chunkhash].chunk.js',
		filename: IS_PROD ? '[name]-bundle.[chunkhash].js' : '[name]-bundle.js'
	},
	resolve: {
		unsafeCache: true,
		modules: ['node_modules', 'frontend_src/client'],
		extensions: ['*', '.webpack.js', '.web.js', '.js', '.styl'],
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				include: [ DIRS.SRC_CLIENT ],
				use: [
					{
						loader: 'babel-loader',
						options: {
							cacheDirectory: true,
							env: {
								"development": {
									"presets": ["react-hmre"]
								}
							}
						}
					}
				]
			},

			STYLUS_LOADER,

			{
				test: /\.css$/,
				use: [
					{ loader: 'style-loader'},
					{ loader: 'css-loader'}
				]
			},
			{
				test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				use: [
					'url-loader?limit=10000&mimetype=application/font-woff'
				]
			},
			{
				test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				use: ['file-loader']
			},{
				test: /\.(png|jpg|jpeg|gif)$/,
				use: [
					{
						loader: 'url-loader',
						options: {
							name: IS_PROD ? '[hash].[ext]' : '[path][name].[ext]?[hash]',
							limit: 10000,
						}
					}
				]
			}
		]
	},
	plugins: [
		new WebpackMd5Hash(),
		new webpack.LoaderOptionsPlugin({
			options: {
				stylus: {
					sourceMap: !IS_PROD,
					use: [nib(), axis(), rupture()],
					import: path.resolve(__dirname, '../frontend_src/stylus/index.styl'),
					error: IS_PROD,
					compress: IS_PROD,
					'include css': true
				},
				context: DIRS.ROOT
			},
			minimize: IS_PROD,
			debug: !IS_PROD
		}),
		new ProgressPlugin(),
		new webpack.DefinePlugin({
			__DEV__: !IS_PROD,
			__SERVER__: false,
			"process.env.NODE_ENV": (IS_PROD ? JSON.stringify("production") : JSON.stringify("development"))
		}),
		new webpack.ProvidePlugin({
			React: 'react',
			jQuery: 'jquery'
		}),

		new ChunkManifestPlugin({
			filename: "chunk-manifest.json",
			manifestVariable: "webpackManifest"
		}),
		// new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /en/)
		new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
		new BundleTracker({
			path: DIRS.BUILD,
			filename: './webpack-stats.json',
			indent: 2
		})
	]
};

if (IS_PROD){

	console.log('--- CLIENT:PRODUCTION_MODE ---');

	config.entry.vendor = [
		'react', 'react-dom', 'redux',
		'react-redux', 'react-router-redux',
		'history', 'jquery', 'superagent', 'react-helmet',
		'classnames',
		'prop-types',
		'emoji-mart',
		'react-dropzone'
	];

	// Extract out the css builds on client prod, in separate bundles
	// config.resolve.alias = {
	// 	'isomorphic-style-loader': 'style-loader'
	// }

	config.plugins = config.plugins.concat([
		// new ExtractTextPlugin({
		// 	filename: '[name].[chunkhash].css',
		// 	allChunks: true
		// }),
		new OfflinePlugin({
			caches: {
				main: [
					'*.chunk.js',
					':rest:'
				],
				additional: [':externals:'],
				optional: [

				]
			},
			relativePaths: false,
			safeToUseOptionalCaches: true,
			externals: [
				'vendor/font-awesome/fonts/fontawesome-webfont.woff2?v=4.7.0',
				'vendor/animate.css',
				'vendor/font-awesome/css/font-awesome.css',
				'vendor/pace/themes/red/pace-theme-flash.css',
				'vendor/pace/pace.min.js',
				'vendor/nprogress/nprogress.js',
				'vendor/nprogress/nprogress.css'
			],
			ServiceWorker: {
				output: '../../templates/sw.js',
				publicPath: '/sw.js',
				events: true
			}
		}),
		new webpack.NormalModuleReplacementPlugin(
			/\.\/SyncRouteConfig/,
			'./AsyncRouteConfig'
		),
		new webpack.optimize.CommonsChunkPlugin({
			name: ['vendor', 'manifest'],
			filename: IS_PROD
				? '[name]-bundle.[chunkhash].js'
				: '[name]-bundle.js'
		}),
		new webpack.optimize.UglifyJsPlugin({
			beautify: false,
			mangle: {
				screw_ie8: true,
				keep_fnames: true
			},
			compress: {
				screw_ie8: true,
				warnings: false,
				dead_code: true,
				conditionals: true,
				booleans: true,
				unused: true,
				join_vars: true,
				drop_console: true,
				sequences: true
			},
			comments: false,
			sourceMap: false
		}),
		new webpack.HashedModuleIdsPlugin(),
		// new webpack.DllReferencePlugin({
		// 	context: DIRS.SRC_CLIENT,
		// 	manifest: require(DIRS.BUILD_PUBLIC + '/dll/vendor-manifest.json')
		// }),
		new webpack.optimize.AggressiveMergingPlugin(),
	]);
} else {
	config.entry.main.unshift(
		'webpack-dev-server/client?http://localhost:3000',
		'webpack/hot/only-dev-server',
	)
	config.output.publicPath = 'http://localhost:3000/assets/bundles/'
	// config.entry.main.unshift('react-hot-loader/patch')
	config.plugins = config.plugins.concat([
		// new webpack.NamedModulesPlugin(),
		// new ExtractTextPlugin({
		// 	filename: '[name].css',
		// 	allChunks: true
		// }),
		//new webpack.DllReferencePlugin({
		//	context: DIRS.SRC_CLIENT,
		//	manifest: require(DIRS.BUILD_PUBLIC + '/dll/vendor-manifest.json')
		//}),
		new webpack.HotModuleReplacementPlugin(),
		new webpack.NoEmitOnErrorsPlugin()
	]);
}


module.exports = config;
