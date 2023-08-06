Object.defineProperty(exports, "__esModule", { value: true });
exports.extraQueryParameter = exports.emailQueryParameter = void 0;
var tslib_1 = require("tslib");
var getCookie_1 = tslib_1.__importDefault(require("app/utils/getCookie"));
// return email query parameter
function emailQueryParameter() {
    var email = localStorage.getItem('email');
    var queryParameter = email ? "?email=" + email : '';
    return queryParameter;
}
exports.emailQueryParameter = emailQueryParameter;
// return extra query depending, depending on if used in getStartedUrl
function extraQueryParameter(getStarted) {
    var email = localStorage.getItem('email');
    var extraQueryString = getCookie_1.default('extra_query_string');
    // cookies that have = sign are quotes so extra quotes need to be removed
    var extraQuery = extraQueryString ? extraQueryString.replaceAll('"', '') : '';
    if (getStarted) {
        var emailSeparator = email ? '&' : '?';
        var getStartedSeparator = extraQueryString ? emailSeparator : '';
        return getStartedSeparator + extraQuery;
    }
    var extraSeparator = extraQueryString ? "?" : '';
    return extraSeparator + extraQuery;
}
exports.extraQueryParameter = extraQueryParameter;
//# sourceMappingURL=demoMode.jsx.map