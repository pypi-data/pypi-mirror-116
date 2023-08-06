'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
exports.getNewLine = exports.killPid = exports.isAlive = exports.getTunerProc = exports.getCmdPy = exports.getVersion = exports.getLogLevel = exports.randomSelect = exports.randomInt = exports.uniqueString = exports.cleanupUnitTest = exports.parseArg = exports.prepareUnitTest = exports.delay = exports.mkDirPSync = exports.mkDirP = exports.isPortOpen = exports.getFreePort = exports.withLockSync = exports.unixPathJoin = exports.getIPV4Address = exports.getDefaultDatabaseDir = exports.getJobCancelStatus = exports.getExperimentRootDir = exports.getLogDir = exports.getExperimentsInfoPath = exports.getCheckpointDir = exports.getMsgDispatcherCommand = exports.generateParamFileName = exports.countFilesRecursively = exports.importModule = void 0;
const assert = require("assert");
const crypto_1 = require("crypto");
const cpp = require("child-process-promise");
const cp = require("child_process");
const child_process_1 = require("child_process");
const dgram = require("dgram");
const fs = require("fs");
const net = require("net");
const os = require("os");
const path = require("path");
const timersPromises = require("timers/promises");
const lockfile = require("lockfile");
const ts_deferred_1 = require("ts-deferred");
const typescript_ioc_1 = require("typescript-ioc");
const glob = require("glob");
const datastore_1 = require("./datastore");
const experimentStartupInfo_1 = require("./experimentStartupInfo");
const manager_1 = require("./manager");
const experimentManager_1 = require("./experimentManager");
const trainingService_1 = require("./trainingService");
function getExperimentRootDir() {
    return experimentStartupInfo_1.getExperimentStartupInfo().logDir;
}
exports.getExperimentRootDir = getExperimentRootDir;
function getLogDir() {
    return path.join(getExperimentRootDir(), 'log');
}
exports.getLogDir = getLogDir;
function getLogLevel() {
    return experimentStartupInfo_1.getExperimentStartupInfo().logLevel;
}
exports.getLogLevel = getLogLevel;
function getDefaultDatabaseDir() {
    return path.join(getExperimentRootDir(), 'db');
}
exports.getDefaultDatabaseDir = getDefaultDatabaseDir;
function getCheckpointDir() {
    return path.join(getExperimentRootDir(), 'checkpoint');
}
exports.getCheckpointDir = getCheckpointDir;
function getExperimentsInfoPath() {
    return path.join(os.homedir(), 'nni-experiments', '.experiment');
}
exports.getExperimentsInfoPath = getExperimentsInfoPath;
async function mkDirP(dirPath) {
    await fs.promises.mkdir(dirPath, { recursive: true });
}
exports.mkDirP = mkDirP;
function mkDirPSync(dirPath) {
    fs.mkdirSync(dirPath, { recursive: true });
}
exports.mkDirPSync = mkDirPSync;
const delay = timersPromises.setTimeout;
exports.delay = delay;
function charMap(index) {
    if (index < 26) {
        return index + 97;
    }
    else if (index < 52) {
        return index - 26 + 65;
    }
    else {
        return index - 52 + 48;
    }
}
function uniqueString(len) {
    if (len === 0) {
        return '';
    }
    const byteLength = Math.ceil((Math.log2(52) + Math.log2(62) * (len - 1)) / 8);
    let num = crypto_1.randomBytes(byteLength).reduce((a, b) => a * 256 + b, 0);
    const codes = [];
    codes.push(charMap(num % 52));
    num = Math.floor(num / 52);
    for (let i = 1; i < len; i++) {
        codes.push(charMap(num % 62));
        num = Math.floor(num / 62);
    }
    return String.fromCharCode(...codes);
}
exports.uniqueString = uniqueString;
function randomInt(max) {
    return Math.floor(Math.random() * max);
}
exports.randomInt = randomInt;
function randomSelect(a) {
    assert(a !== undefined);
    return a[Math.floor(Math.random() * a.length)];
}
exports.randomSelect = randomSelect;
function parseArg(names) {
    if (process.argv.length >= 4) {
        for (let i = 2; i < process.argv.length - 1; i++) {
            if (names.includes(process.argv[i])) {
                return process.argv[i + 1];
            }
        }
    }
    return '';
}
exports.parseArg = parseArg;
function getCmdPy() {
    let cmd = 'python3';
    if (process.platform === 'win32') {
        cmd = 'python';
    }
    return cmd;
}
exports.getCmdPy = getCmdPy;
function getMsgDispatcherCommand(expParams) {
    const clonedParams = Object.assign({}, expParams);
    delete clonedParams.searchSpace;
    return `${getCmdPy()} -m nni --exp_params ${Buffer.from(JSON.stringify(clonedParams)).toString('base64')}`;
}
exports.getMsgDispatcherCommand = getMsgDispatcherCommand;
function generateParamFileName(hyperParameters) {
    assert(hyperParameters !== undefined);
    assert(hyperParameters.index >= 0);
    let paramFileName;
    if (hyperParameters.index == 0) {
        paramFileName = 'parameter.cfg';
    }
    else {
        paramFileName = `parameter_${hyperParameters.index}.cfg`;
    }
    return paramFileName;
}
exports.generateParamFileName = generateParamFileName;
function prepareUnitTest() {
    typescript_ioc_1.Container.snapshot(datastore_1.Database);
    typescript_ioc_1.Container.snapshot(datastore_1.DataStore);
    typescript_ioc_1.Container.snapshot(trainingService_1.TrainingService);
    typescript_ioc_1.Container.snapshot(manager_1.Manager);
    typescript_ioc_1.Container.snapshot(experimentManager_1.ExperimentManager);
    const logLevel = parseArg(['--log_level', '-ll']);
    experimentStartupInfo_1.setExperimentStartupInfo(true, 'unittest', 8080, 'unittest', undefined, logLevel);
    mkDirPSync(getLogDir());
    const sqliteFile = path.join(getDefaultDatabaseDir(), 'nni.sqlite');
    try {
        fs.unlinkSync(sqliteFile);
    }
    catch (err) {
    }
}
exports.prepareUnitTest = prepareUnitTest;
function cleanupUnitTest() {
    typescript_ioc_1.Container.restore(manager_1.Manager);
    typescript_ioc_1.Container.restore(trainingService_1.TrainingService);
    typescript_ioc_1.Container.restore(datastore_1.DataStore);
    typescript_ioc_1.Container.restore(datastore_1.Database);
    typescript_ioc_1.Container.restore(experimentManager_1.ExperimentManager);
    const logLevel = parseArg(['--log_level', '-ll']);
    experimentStartupInfo_1.setExperimentStartupInfo(true, 'unittest', 8080, 'unittest', undefined, logLevel);
}
exports.cleanupUnitTest = cleanupUnitTest;
let cachedIpv4Address = null;
async function getIPV4Address() {
    if (cachedIpv4Address !== null) {
        return cachedIpv4Address;
    }
    const socket = dgram.createSocket('udp4');
    socket.connect(1, '192.0.2.0');
    for (let i = 0; i < 10; i++) {
        await timersPromises.setTimeout(1);
        try {
            cachedIpv4Address = socket.address().address;
            socket.close();
            return cachedIpv4Address;
        }
        catch (error) {
        }
    }
    cachedIpv4Address = socket.address().address;
    socket.close();
    return cachedIpv4Address;
}
exports.getIPV4Address = getIPV4Address;
function getJobCancelStatus(isEarlyStopped) {
    return isEarlyStopped ? 'EARLY_STOPPED' : 'USER_CANCELED';
}
exports.getJobCancelStatus = getJobCancelStatus;
function countFilesRecursively(directory) {
    if (!fs.existsSync(directory)) {
        throw Error(`Direcotory ${directory} doesn't exist`);
    }
    const deferred = new ts_deferred_1.Deferred();
    let timeoutId;
    const delayTimeout = new Promise((resolve, reject) => {
        timeoutId = setTimeout(() => {
            reject(new Error(`Timeout: path ${directory} has too many files`));
        }, 5000);
    });
    let fileCount = -1;
    let cmd;
    if (process.platform === "win32") {
        cmd = `powershell "Get-ChildItem -Path ${directory} -Recurse -File | Measure-Object | %{$_.Count}"`;
    }
    else {
        cmd = `find ${directory} -type f | wc -l`;
    }
    cpp.exec(cmd).then((result) => {
        if (result.stdout && parseInt(result.stdout)) {
            fileCount = parseInt(result.stdout);
        }
        deferred.resolve(fileCount);
    });
    return Promise.race([deferred.promise, delayTimeout]).finally(() => {
        clearTimeout(timeoutId);
    });
}
exports.countFilesRecursively = countFilesRecursively;
async function getVersion() {
    const deferred = new ts_deferred_1.Deferred();
    Promise.resolve().then(() => require(path.join(__dirname, '..', 'package.json'))).then((pkg) => {
        deferred.resolve(pkg.version);
    }).catch(() => {
        deferred.resolve('999.0.0-developing');
    });
    return deferred.promise;
}
exports.getVersion = getVersion;
function getTunerProc(command, stdio, newCwd, newEnv, newShell = true, isDetached = false) {
    let cmd = command;
    let arg = [];
    if (process.platform === "win32") {
        cmd = command.split(" ", 1)[0];
        arg = command.substr(cmd.length + 1).split(" ");
        newShell = false;
        isDetached = true;
    }
    const tunerProc = child_process_1.spawn(cmd, arg, {
        stdio,
        cwd: newCwd,
        env: newEnv,
        shell: newShell,
        detached: isDetached
    });
    return tunerProc;
}
exports.getTunerProc = getTunerProc;
async function isAlive(pid) {
    const deferred = new ts_deferred_1.Deferred();
    let alive = false;
    if (process.platform === 'win32') {
        try {
            const str = cp.execSync(`powershell.exe Get-Process -Id ${pid} -ErrorAction SilentlyContinue`).toString();
            if (str) {
                alive = true;
            }
        }
        catch (error) {
        }
    }
    else {
        try {
            await cpp.exec(`kill -0 ${pid}`);
            alive = true;
        }
        catch (error) {
        }
    }
    deferred.resolve(alive);
    return deferred.promise;
}
exports.isAlive = isAlive;
async function killPid(pid) {
    const deferred = new ts_deferred_1.Deferred();
    try {
        if (process.platform === "win32") {
            await cpp.exec(`cmd.exe /c taskkill /PID ${pid} /F`);
        }
        else {
            await cpp.exec(`kill -9 ${pid}`);
        }
    }
    catch (error) {
    }
    deferred.resolve();
    return deferred.promise;
}
exports.killPid = killPid;
function getNewLine() {
    if (process.platform === "win32") {
        return "\r\n";
    }
    else {
        return "\n";
    }
}
exports.getNewLine = getNewLine;
function unixPathJoin(...paths) {
    const dir = paths.filter((path) => path !== '').join('/');
    if (dir === '')
        return '.';
    return dir;
}
exports.unixPathJoin = unixPathJoin;
function withLockSync(func, filePath, lockOpts, ...args) {
    const lockName = path.join(path.dirname(filePath), path.basename(filePath) + `.lock.${process.pid}`);
    if (typeof lockOpts.stale === 'number') {
        const lockPath = path.join(path.dirname(filePath), path.basename(filePath) + '.lock.*');
        const lockFileNames = glob.sync(lockPath);
        const canLock = lockFileNames.map((fileName) => {
            return fs.existsSync(fileName) && Date.now() - fs.statSync(fileName).mtimeMs < lockOpts.stale;
        }).filter(unexpired => unexpired === true).length === 0;
        if (!canLock) {
            throw new Error('File has been locked.');
        }
    }
    lockfile.lockSync(lockName, lockOpts);
    const result = func(...args);
    lockfile.unlockSync(lockName);
    return result;
}
exports.withLockSync = withLockSync;
async function isPortOpen(host, port) {
    return new Promise((resolve, reject) => {
        try {
            const stream = net.createConnection(port, host);
            const id = setTimeout(() => {
                stream.destroy();
                resolve(false);
            }, 1000);
            stream.on('connect', () => {
                clearTimeout(id);
                stream.destroy();
                resolve(true);
            });
            stream.on('error', () => {
                clearTimeout(id);
                stream.destroy();
                resolve(false);
            });
        }
        catch (error) {
            reject(error);
        }
    });
}
exports.isPortOpen = isPortOpen;
async function getFreePort(host, start, end) {
    if (start > end) {
        throw new Error(`no more free port`);
    }
    if (await isPortOpen(host, start)) {
        return await getFreePort(host, start + 1, end);
    }
    else {
        return start;
    }
}
exports.getFreePort = getFreePort;
function importModule(modulePath) {
    module.paths.unshift(path.dirname(modulePath));
    return require(path.basename(modulePath));
}
exports.importModule = importModule;
