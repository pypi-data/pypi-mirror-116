"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createEnvironmentService = void 0;
const amlEnvironmentService_1 = require("./amlEnvironmentService");
const openPaiEnvironmentService_1 = require("./openPaiEnvironmentService");
const localEnvironmentService_1 = require("./localEnvironmentService");
const remoteEnvironmentService_1 = require("./remoteEnvironmentService");
const kubeflowEnvironmentService_1 = require("./kubernetes/kubeflowEnvironmentService");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const nniConfig_1 = require("../../../common/nniConfig");
const utils_1 = require("../../../common/utils");
async function createEnvironmentService(name, config) {
    const info = experimentStartupInfo_1.ExperimentStartupInfo.getInstance();
    switch (name) {
        case 'local':
            return new localEnvironmentService_1.LocalEnvironmentService(config, info);
        case 'remote':
            return new remoteEnvironmentService_1.RemoteEnvironmentService(config, info);
        case 'aml':
            return new amlEnvironmentService_1.AMLEnvironmentService(config, info);
        case 'openpai':
            return new openPaiEnvironmentService_1.OpenPaiEnvironmentService(config, info);
        case 'kubeflow':
            return new kubeflowEnvironmentService_1.KubeflowEnvironmentService(config, info);
    }
    const esConfig = await nniConfig_1.getCustomEnvironmentServiceConfig(name);
    if (esConfig === null) {
        throw new Error(`${name} is not a supported training service!`);
    }
    const esModule = utils_1.importModule(esConfig.nodeModulePath);
    const esClass = esModule[esConfig.nodeClassName];
    return new esClass(config, info);
}
exports.createEnvironmentService = createEnvironmentService;
