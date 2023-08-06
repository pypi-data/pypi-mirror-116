var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.expandKeys = exports.getRequestMessages = exports.dropDownItems = exports.customRepoTypeLabel = void 0;
var tslib_1 = require("tslib");
var forEach_1 = tslib_1.__importDefault(require("lodash/forEach"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var locale_1 = require("app/locale");
var debugFiles_1 = require("app/types/debugFiles");
exports.customRepoTypeLabel = (_a = {},
    _a[debugFiles_1.CustomRepoType.APP_STORE_CONNECT] = 'App Store Connect',
    _a[debugFiles_1.CustomRepoType.HTTP] = 'SymbolServer (HTTP)',
    _a[debugFiles_1.CustomRepoType.S3] = 'Amazon S3',
    _a[debugFiles_1.CustomRepoType.GCS] = 'Google Cloud Storage',
    _a);
exports.dropDownItems = [
    {
        value: debugFiles_1.CustomRepoType.S3,
        label: exports.customRepoTypeLabel[debugFiles_1.CustomRepoType.S3],
        searchKey: locale_1.t('aws amazon s3 bucket'),
    },
    {
        value: debugFiles_1.CustomRepoType.GCS,
        label: exports.customRepoTypeLabel[debugFiles_1.CustomRepoType.GCS],
        searchKey: locale_1.t('gcs google cloud storage bucket'),
    },
    {
        value: debugFiles_1.CustomRepoType.HTTP,
        label: exports.customRepoTypeLabel[debugFiles_1.CustomRepoType.HTTP],
        searchKey: locale_1.t('http symbol server ssqp symstore symsrv'),
    },
];
function getRequestMessages(updatedRepositoriesQuantity, repositoriesQuantity) {
    if (updatedRepositoriesQuantity > repositoriesQuantity) {
        return {
            successMessage: locale_1.t('Successfully added custom repository'),
            errorMessage: locale_1.t('An error occurred while adding a new custom repository'),
        };
    }
    if (updatedRepositoriesQuantity < repositoriesQuantity) {
        return {
            successMessage: locale_1.t('Successfully removed custom repository'),
            errorMessage: locale_1.t('An error occurred while removing the custom repository'),
        };
    }
    return {
        successMessage: locale_1.t('Successfully updated custom repository'),
        errorMessage: locale_1.t('An error occurred while updating the custom repository'),
    };
}
exports.getRequestMessages = getRequestMessages;
function expandKeys(obj) {
    var result = {};
    forEach_1.default(obj, function (value, key) {
        set_1.default(result, key.split('.'), value);
    });
    return result;
}
exports.expandKeys = expandKeys;
//# sourceMappingURL=utils.jsx.map