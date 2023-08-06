Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var api_1 = require("app/api");
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var BASE_DELAY = 3000;
var MAX_DELAY = 60000;
var CursorPoller = /** @class */ (function () {
    function CursorPoller(options) {
        this.api = new api_1.Client();
        this.timeoutId = null;
        this.lastRequest = null;
        this.active = true;
        this.reqsWithoutData = 0;
        this.options = options;
        this.pollingEndpoint = options.endpoint;
    }
    CursorPoller.prototype.getDelay = function () {
        var delay = BASE_DELAY * (this.reqsWithoutData + 1);
        return Math.min(delay, MAX_DELAY);
    };
    CursorPoller.prototype.setEndpoint = function (url) {
        this.pollingEndpoint = url;
    };
    CursorPoller.prototype.enable = function () {
        this.active = true;
        if (!this.timeoutId) {
            this.timeoutId = window.setTimeout(this.poll.bind(this), this.getDelay());
        }
    };
    CursorPoller.prototype.disable = function () {
        this.active = false;
        if (this.timeoutId) {
            window.clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }
        if (this.lastRequest) {
            this.lastRequest.cancel();
        }
    };
    CursorPoller.prototype.poll = function () {
        var _this = this;
        this.lastRequest = this.api.request(this.pollingEndpoint, {
            success: function (data, _, resp) {
                var _a;
                // cancel in progress operation if disabled
                if (!_this.active) {
                    return;
                }
                // if theres no data, nothing changes
                if (!data || !data.length) {
                    _this.reqsWithoutData += 1;
                    return;
                }
                if (_this.reqsWithoutData > 0) {
                    _this.reqsWithoutData -= 1;
                }
                var linksHeader = (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null;
                var links = parseLinkHeader_1.default(linksHeader);
                _this.pollingEndpoint = links.previous.href;
                _this.options.success(data, linksHeader);
            },
            error: function (resp) {
                if (!resp) {
                    return;
                }
                // If user does not have access to the endpoint, we should halt polling
                // These errors could mean:
                // * the user lost access to a project
                // * project was renamed
                // * user needs to reauth
                if (resp.status === 404 || resp.status === 403 || resp.status === 401) {
                    _this.disable();
                }
            },
            complete: function () {
                _this.lastRequest = null;
                if (_this.active) {
                    _this.timeoutId = window.setTimeout(_this.poll.bind(_this), _this.getDelay());
                }
            },
        });
    };
    return CursorPoller;
}());
exports.default = CursorPoller;
//# sourceMappingURL=cursorPoller.jsx.map