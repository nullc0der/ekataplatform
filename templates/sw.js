var __wpo = {"assets":{"main":["/statics/bundles/Groups-Members-Management.ee3c035ca6cdb0204046.chunk.js","/statics/bundles/Group-Posts.48c371a2f5ebf8e804ee.chunk.js","/statics/bundles/Groups-Settings.e9b324ac1cef1221cdfa.chunk.js","/statics/bundles/MessengerPage.c854f35ec932408633ed.chunk.js","/statics/bundles/PublicMembers.89c0d03182aa587f1d85.chunk.js","/statics/bundles/GroupsPage.e88ad5654b2bcbea7080.chunk.js","/statics/bundles/HomePage.cae49dcba24b5b3865fc.chunk.js","/statics/bundles/ErrorPage.3d2281bffd71a4adaf7e.chunk.js","/statics/bundles/main-bundle.7301a12ae6ee9051858d.js","/statics/bundles/vendor-bundle.d5c89901f10c42c07c00.js","/statics/bundles/chunk-manifest.json","/statics/bundles/manifest-bundle.d41d8cd98f00b204e980.js"],"additional":["/statics/bundles/vendor/font-awesome/fonts/fontawesome-webfont.woff2?v=4.7.0","/statics/bundles/vendor/animate.css","/statics/bundles/vendor/font-awesome/css/font-awesome.css","/statics/bundles/vendor/pace/themes/red/pace-theme-flash.css","/statics/bundles/vendor/pace/pace.min.js","/statics/bundles/vendor/nprogress/nprogress.js","/statics/bundles/vendor/nprogress/nprogress.css"],"optional":[]},"externals":["/statics/bundles/vendor/font-awesome/fonts/fontawesome-webfont.woff2?v=4.7.0","/statics/bundles/vendor/animate.css","/statics/bundles/vendor/font-awesome/css/font-awesome.css","/statics/bundles/vendor/pace/themes/red/pace-theme-flash.css","/statics/bundles/vendor/pace/pace.min.js","/statics/bundles/vendor/nprogress/nprogress.js","/statics/bundles/vendor/nprogress/nprogress.css"],"hashesMap":{"43feb38a5731838f1820ebfe20d6f30b0b44c0c2":"/statics/bundles/Groups-Members-Management.ee3c035ca6cdb0204046.chunk.js","989bbdb793aa1d68dc5fed545327eba645306a98":"/statics/bundles/Group-Posts.48c371a2f5ebf8e804ee.chunk.js","eee137575ab98365cd22e7c1ba5e1550ad674f15":"/statics/bundles/Groups-Settings.e9b324ac1cef1221cdfa.chunk.js","461b73c3d2e8a71d8d14e86d04ecb76eb65891d0":"/statics/bundles/MessengerPage.c854f35ec932408633ed.chunk.js","5d335bf78c525f8df14a40a83ee8ac1decb1f34f":"/statics/bundles/PublicMembers.89c0d03182aa587f1d85.chunk.js","ab6fdd0dffd1ecd9b60c38863cdcf411f52985a2":"/statics/bundles/GroupsPage.e88ad5654b2bcbea7080.chunk.js","e52e472b3e59d7c5398a3d1907b278b67a876c6d":"/statics/bundles/HomePage.cae49dcba24b5b3865fc.chunk.js","6ca02b274220f56b4007377a8db2515c04b87c2a":"/statics/bundles/ErrorPage.3d2281bffd71a4adaf7e.chunk.js","8a75a792355b581fc887d634cb6a53148e547682":"/statics/bundles/main-bundle.7301a12ae6ee9051858d.js","e0ddcdceed5ac736b542a32dce68db6bb613d108":"/statics/bundles/vendor-bundle.d5c89901f10c42c07c00.js","9528c0649833b86f1a4925eda2b949c7f6bfc898":"/statics/bundles/chunk-manifest.json","08f17548b7e51bd9d25c0826c18279ea6cd1caa5":"/statics/bundles/manifest-bundle.d41d8cd98f00b204e980.js"},"strategy":"changed","responseStrategy":"cache-first","version":"2018-3-10 16:14:44","name":"webpack-offline","pluginVersion":"4.7.0","relativePaths":false};

!function(e){function __webpack_require__(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,__webpack_require__),r.l=!0,r.exports}var n={};__webpack_require__.m=e,__webpack_require__.c=n,__webpack_require__.i=function(e){return e},__webpack_require__.d=function(e,n,t){__webpack_require__.o(e,n)||Object.defineProperty(e,n,{configurable:!1,enumerable:!0,get:t})},__webpack_require__.n=function(e){var n=e&&e.__esModule?function(){return e.default}:function(){return e};return __webpack_require__.d(n,"a",n),n},__webpack_require__.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},__webpack_require__.p="/statics/bundles/",__webpack_require__(__webpack_require__.s="NmIi")}({NmIi:function(e,n,t){"use strict";function cachesMatch(e,n){return caches.match(e,{cacheName:n}).then(function(t){return isNotRedirectedResponse()?t:fixRedirectedResponse(t).then(function(t){return caches.open(n).then(function(n){return n.put(e,t)}).then(function(){return t})})}).catch(function(){})}function applyCacheBust(e,n){return e+(-1!==e.indexOf("?")?"&":"?")+"__uncache="+encodeURIComponent(n)}function isNavigateRequest(e){return"navigate"===e.mode||e.headers.get("Upgrade-Insecure-Requests")||-1!==(e.headers.get("Accept")||"").indexOf("text/html")}function isNotRedirectedResponse(e){return!e||!e.redirected||!e.ok||"opaqueredirect"===e.type}function fixRedirectedResponse(e){return isNotRedirectedResponse(e)?Promise.resolve(e):("body"in e?Promise.resolve(e.body):e.blob()).then(function(n){return new Response(n,{headers:e.headers,status:e.status})})}function copyObject(e){return Object.keys(e).reduce(function(n,t){return n[t]=e[t],n},{})}function logGroup(e,n){n.forEach(function(e){})}if(void 0===r)var r=!1;!function(e,n){function cacheAdditional(){if(!c.additional.length)return Promise.resolve();var e=void 0;return e="changed"===a?cacheChanged("additional"):cacheAssets("additional"),e.catch(function(e){})}function cacheAssets(n){var t=c[n];return caches.open(l).then(function(n){return addAllNormalized(n,t,{bust:e.version,request:e.prefetchRequest})}).then(function(){logGroup("Cached assets: "+n,t)}).catch(function(e){throw e})}function cacheChanged(n){return getLastCache().then(function(t){if(!t)return cacheAssets(n);var r=t[0],a=t[1],i=t[2],o=i.hashmap,u=i.version;if(!i.hashmap||u===e.version)return cacheAssets(n);var f=Object.keys(o).map(function(e){return o[e]}),h=a.map(function(e){var n=new URL(e.url);return n.search="",n.toString()}),d=c[n],p=[],v=d.filter(function(e){return-1===h.indexOf(e)||-1===f.indexOf(e)});Object.keys(s).forEach(function(e){var n=s[e];if(-1!==d.indexOf(n)&&-1===v.indexOf(n)&&-1===p.indexOf(n)){var t=o[e];t&&-1!==h.indexOf(t)?p.push([t,n]):v.push(n)}}),logGroup("Changed assets: "+n,v),logGroup("Moved assets: "+n,p);var _=Promise.all(p.map(function(e){return r.match(e[0]).then(function(n){return[e[1],n]})}));return caches.open(l).then(function(n){var t=_.then(function(e){return Promise.all(e.map(function(e){return n.put(e[0],e[1])}))});return Promise.all([t,addAllNormalized(n,v,{bust:e.version,request:e.prefetchRequest})])})})}function deleteObsolete(){return caches.keys().then(function(e){var n=e.map(function(e){if(0===e.indexOf(f)&&0!==e.indexOf(l))return caches.delete(e)});return Promise.all(n)})}function getLastCache(){return caches.keys().then(function(e){for(var n=e.length,t=void 0;n--&&(t=e[n],0!==t.indexOf(f)););if(t){var r=void 0;return caches.open(t).then(function(e){return r=e,e.match(new URL(d,location).toString())}).then(function(e){if(e)return Promise.all([r,r.keys(),e.json()])})}})}function storeCacheData(){return caches.open(l).then(function(n){var t=new Response(JSON.stringify({version:e.version,hashmap:s}));return n.put(new URL(d,location).toString(),t)})}function cacheFirstResponse(e,n,t){return cachesMatch(t,l).then(function(r){return r||fetch(e.request).then(function(e){return e.ok?(t===n&&function(){var t=e.clone();caches.open(l).then(function(e){return e.put(n,t)}).then(function(){})}(),e):e})})}function networkFirstResponse(e,n,t){return fetch(e.request).then(function(e){if(e.ok)return e;throw new Error("Response is not ok")}).catch(function(){return cachesMatch(t,l)})}function handleNavigateFallback(e){return e.catch(function(){}).then(function(e){var n=e&&e.ok,t=e&&"opaqueredirect"===e.type;return n||t&&!_?e:cachesMatch(v,l)})}function addAllNormalized(e,n,t){var r=!1!==t.allowLoaders,a=t&&t.bust,i=t.request||{credentials:"omit",mode:"cors"};return Promise.all(n.map(function(e){return a&&(e=applyCacheBust(e,a)),fetch(e,i).then(fixRedirectedResponse)})).then(function(a){if(a.some(function(e){return!e.ok}))return Promise.reject(new Error("Wrong response status"));var i=[],c=a.map(function(t,a){return r&&i.push(extractAssetsWithLoaders(n[a],t)),e.put(n[a],t)});return i.length?function(){var r=copyObject(t);r.allowLoaders=!1;var a=c;c=Promise.all(i).then(function(t){var i=[].concat.apply([],t);return n.length&&(a=a.concat(addAllNormalized(e,i,r))),Promise.all(a)})}():c=Promise.all(c),c})}function extractAssetsWithLoaders(e,n){var r=Object.keys(o).map(function(r){if(-1!==o[r].indexOf(e)&&t[r])return t[r](n.clone())}).filter(function(e){return!!e});return Promise.all(r).then(function(e){return[].concat.apply([],e)})}function matchCacheMap(e){var n=e.url,t=new URL(n),a=void 0;a="navigate"===e.mode?"navigate":t.origin===location.origin?"same-origin":"cross-origin";for(var i=0;i<r.length;i++){var c=r[i];if(c&&(!c.requestTypes||-1!==c.requestTypes.indexOf(a))){var o=void 0;if((o="function"==typeof c.match?c.match(t,e):n.replace(c.match,c.to))&&o!==n)return o}}}var t=n.loaders,r=n.cacheMaps,a=e.strategy,i=e.responseStrategy,c=e.assets,o=e.loaders||{},s=e.hashesMap,u=e.externals,f=e.name,h=e.version,l=f+":"+h,d="__offline_webpack__data";!function(){Object.keys(c).forEach(function(e){c[e]=c[e].map(function(e){var n=new URL(e,location);return-1===u.indexOf(e)?n.search="":n.hash="",n.toString()})}),Object.keys(o).forEach(function(e){o[e]=o[e].map(function(e){var n=new URL(e,location);return-1===u.indexOf(e)?n.search="":n.hash="",n.toString()})}),s=Object.keys(s).reduce(function(e,n){var t=new URL(s[n],location);return t.search="",e[n]=t.toString(),e},{}),u=u.map(function(e){var n=new URL(e,location);return n.hash="",n.toString()})}();var p=[].concat(c.main,c.additional,c.optional),v=e.navigateFallbackURL,_=e.navigateFallbackForRedirects;self.addEventListener("install",function(e){var n=void 0;n="changed"===a?cacheChanged("main"):cacheAssets("main"),e.waitUntil(n)}),self.addEventListener("activate",function(e){var n=cacheAdditional();n=n.then(storeCacheData),n=n.then(deleteObsolete),n=n.then(function(){if(self.clients&&self.clients.claim)return self.clients.claim()}),e.waitUntil(n)}),self.addEventListener("fetch",function(e){var n=e.request.url,t=new URL(n),r=void 0;-1!==u.indexOf(n)?r=n:(t.search="",r=t.toString());var a="GET"===e.request.method,c=-1!==p.indexOf(r),o=r;if(!c){var s=matchCacheMap(e.request);s&&(o=s,c=!0)}if(!c&&a&&v&&isNavigateRequest(e.request))return void e.respondWith(handleNavigateFallback(fetch(e.request)));if(!c||!a)return void(t.origin!==location.origin&&-1!==navigator.userAgent.indexOf("Firefox/44.")&&e.respondWith(fetch(e.request)));var f=void 0;f="network-first"===i?networkFirstResponse(e,r,o):cacheFirstResponse(e,r,o),v&&isNavigateRequest(e.request)&&(f=handleNavigateFallback(f)),e.respondWith(f)}),self.addEventListener("message",function(e){var n=e.data;if(n)switch(n.action){case"skipWaiting":self.skipWaiting&&self.skipWaiting()}})}(__wpo,{loaders:{},cacheMaps:[]}),e.exports=t("dM3S")},dM3S:function(e,n){}});