'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCustomEnvironmentServiceConfig = void 0;
const fs = require("fs");
const path = require("path");
const util_1 = require("util");
const pythonScript_1 = require("./pythonScript");
const readFile = util_1.promisify(fs.readFile);
async function readConfigFile(fileName) {
    const script = 'import nni.runtime.config ; print(nni.runtime.config.get_config_directory())';
    const configDir = (await pythonScript_1.runPythonScript(script)).trim();
    const stream = await readFile(path.join(configDir, fileName));
    return stream.toString();
}
async function getCustomEnvironmentServiceConfig(name) {
    const configJson = await readConfigFile('training_services.json');
    const config = JSON.parse(configJson);
    if (config[name] === undefined) {
        return null;
    }
    return {
        name,
        nodeModulePath: config[name].nodeModulePath,
        nodeClassName: config[name].nodeClassName,
    };
}
exports.getCustomEnvironmentServiceConfig = getCustomEnvironmentServiceConfig;
