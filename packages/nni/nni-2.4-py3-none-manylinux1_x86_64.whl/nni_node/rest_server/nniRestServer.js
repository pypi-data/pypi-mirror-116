'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.NNIRestServer = void 0;
const bodyParser = require("body-parser");
const express = require("express");
const httpProxy = require("http-proxy");
const path = require("path");
const component = require("../common/component");
const restServer_1 = require("../common/restServer");
const utils_1 = require("../common/utils");
const restHandler_1 = require("./restHandler");
const experimentStartupInfo_1 = require("../common/experimentStartupInfo");
let NNIRestServer = class NNIRestServer extends restServer_1.RestServer {
    LOGS_ROOT_URL = '/logs';
    netronProxy = null;
    API_ROOT_URL = '/api/v1/nni';
    constructor() {
        super();
        this.API_ROOT_URL = experimentStartupInfo_1.getAPIRootUrl();
        this.netronProxy = httpProxy.createProxyServer();
    }
    registerRestHandler() {
        this.app.use(experimentStartupInfo_1.getPrefixUrl(), express.static('static'));
        this.app.use(bodyParser.json({ limit: '50mb' }));
        this.app.use(this.API_ROOT_URL, restHandler_1.createRestHandler(this));
        this.app.use(this.LOGS_ROOT_URL, express.static(utils_1.getLogDir()));
        this.app.all('/netron/*', (req, res) => {
            delete req.headers.host;
            req.url = req.url.replace('/netron', '/');
            this.netronProxy.web(req, res, {
                changeOrigin: true,
                target: 'https://netron.app'
            });
        });
        this.app.get(`${experimentStartupInfo_1.getPrefixUrl()}/*`, (req, res) => {
            res.sendFile(path.resolve('static/index.html'));
        });
    }
};
NNIRestServer = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], NNIRestServer);
exports.NNIRestServer = NNIRestServer;
