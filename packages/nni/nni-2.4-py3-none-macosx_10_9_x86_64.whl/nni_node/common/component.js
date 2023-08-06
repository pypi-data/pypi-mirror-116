'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
exports.get = exports.Singleton = exports.Inject = exports.Container = exports.Provides = void 0;
const ioc = require("typescript-ioc");
const Inject = ioc.Inject;
exports.Inject = Inject;
const Singleton = ioc.Singleton;
exports.Singleton = Singleton;
const Container = ioc.Container;
exports.Container = Container;
const Provides = ioc.Provides;
exports.Provides = Provides;
function get(source) {
    return ioc.Container.get(source);
}
exports.get = get;
