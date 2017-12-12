var path = require('path');

var ROOT = path.resolve(__dirname, '../');

module.exports = {
	ROOT: ROOT,
	SRC: ROOT + '/frontend_src',
	SRC_CLIENT: ROOT + '/frontend_src/client',
	
	BUILD: ROOT + '/static',
	BUILD_PUBLIC: ROOT + '/static/bundles',
	BUILD_VENDOR: ROOT + '/static/bundles/vendor',

	NODE_MODULES: ROOT + '/node_modules',
}
