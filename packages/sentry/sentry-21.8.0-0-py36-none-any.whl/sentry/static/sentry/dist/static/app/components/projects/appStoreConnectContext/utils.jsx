Object.defineProperty(exports, "__esModule", { value: true });
exports.getAppConnectStoreUpdateAlertMessage = exports.appStoreConnectAlertMessage = void 0;
var locale_1 = require("app/locale");
exports.appStoreConnectAlertMessage = {
    iTunesSessionInvalid: locale_1.t('The iTunes session of your configured App Store Connect needs to be refreshed.'),
    appStoreCredentialsInvalid: locale_1.t('The credentials of your configured App Store Connect are invalid.'),
    isTodayAfterItunesSessionRefreshAt: locale_1.t('The iTunes session of your configured App Store Connect will likely expire soon.'),
};
function getAppConnectStoreUpdateAlertMessage(appConnectValidationData) {
    if (appConnectValidationData.promptItunesSession) {
        return exports.appStoreConnectAlertMessage.iTunesSessionInvalid;
    }
    if (appConnectValidationData.appstoreCredentialsValid === false) {
        return exports.appStoreConnectAlertMessage.appStoreCredentialsInvalid;
    }
    return undefined;
}
exports.getAppConnectStoreUpdateAlertMessage = getAppConnectStoreUpdateAlertMessage;
//# sourceMappingURL=utils.jsx.map