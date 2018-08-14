/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./static/js/label.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./static/js/label.js":
/*!****************************!*\
  !*** ./static/js/label.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("axios.defaults.xsrfCookieName = 'csrftoken';\naxios.defaults.xsrfHeaderName = 'X-CSRFToken';\nvar base_url = window.location.href.split('/').slice(3, 5).join('/');\nconst HTTP = axios.create({\n    baseURL: `/api/${base_url}/`,\n})\n\nvar vm = new Vue({\n    el: '#mail-app',\n    delimiters: ['[[', ']]'],\n    data: {\n        labels: [],\n        labelText: '',\n        selectedShortkey: '',\n        backgroundColor: '#209cee',\n        textColor: '#ffffff',\n    },\n\n    methods: {\n        addLabel: function () {\n            var payload = {\n                text: this.labelText,\n                shortcut: this.selectedShortkey,\n                background_color: this.backgroundColor,\n                text_color: this.textColor\n            };\n            HTTP.post('labels/', payload).then(response => {\n                this.reset();\n                this.labels.push(response.data);\n            })\n        },\n        removeLabel: function (label) {\n            var label_id = label.id;\n            HTTP.delete(`labels/${label_id}`).then(response => {\n                var index = this.labels.indexOf(label)\n                this.labels.splice(index, 1)\n            })\n        },\n        reset: function () {\n            this.labelText = '';\n            this.selectedShortkey = '';\n            this.backgroundColor = '#209cee';\n            this.textColor = '#ffffff';\n        }\n    },\n    created: function () {\n        HTTP.get('labels').then(response => {\n            this.labels = response.data\n        })\n    }\n})\n\n//# sourceURL=webpack:///./static/js/label.js?");

/***/ })

/******/ });