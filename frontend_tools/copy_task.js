var path = require('path');
var Promise = require('bluebird');
var fs = Promise.promisifyAll(require('fs-extra'));

var DIRS = require('./dirs');


const normalizePaths = (paths)=> paths.map(x => {
	return [
		path.resolve(DIRS.NODE_MODULES, x[0].replace('~/', './')),
		path.resolve(DIRS.BUILD_VENDOR, x[1].replace('@/', './'))
	]
});

var VENDORS = normalizePaths([

	// FILES
	['~/react/dist/react.js', '@/react.js'],
	['~/react/dist/react-with-addons.js', '@/react-with-addons.js'],
	['~/react-dom/dist/react-dom.js', '@/react-dom.js'],
	['~/redux/dist/redux.js', '@/redux.js'],
	['~/react-redux/dist/react-redux.js', '@/react-redux.js'],
	['~/lodash/lodash.js', '@/lodash.js'],
	['~/animate.css/animate.css', '@/animate.css'],
	['~/font-awesome', '@/font-awesome'],
	['~/nprogress', '@/nprogress'],
	['~/emoji-mart/css/emoji-mart.css', '@/emoji-mart/css/emoji-mart.css']

	// DIRS

]);

function copyItem(paths){
	return fs.copyAsync(paths[0], paths[1])
}

fs.emptyDirAsync(DIRS.BUILD_PUBLIC)
.tap(()=> console.log('  Cleaned ' + DIRS.BUILD_PUBLIC))
.then(()=> Promise.mapSeries(VENDORS, copyItem))
.tap(()=> console.log('  Copied ' + VENDORS.length + ' asset entries.'))
.catch(console.error.bind(console))
