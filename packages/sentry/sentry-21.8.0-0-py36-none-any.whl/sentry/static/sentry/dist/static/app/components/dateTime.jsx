Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var moment_1 = tslib_1.__importDefault(require("moment"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var DateTime = /** @class */ (function (_super) {
    tslib_1.__extends(DateTime, _super);
    function DateTime() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getFormat = function (_a) {
            var clock24Hours = _a.clock24Hours;
            var _b = _this.props, dateOnly = _b.dateOnly, timeOnly = _b.timeOnly, seconds = _b.seconds, shortDate = _b.shortDate, timeAndDate = _b.timeAndDate, format = _b.format;
            if (format) {
                return format;
            }
            // October 26, 2017
            if (dateOnly) {
                return 'LL';
            }
            // Oct 26, 11:30 AM
            if (timeAndDate) {
                if (clock24Hours) {
                    return 'MMM DD, HH:mm';
                }
                return 'MMM DD, LT';
            }
            // 4:57 PM
            if (timeOnly) {
                if (clock24Hours) {
                    return 'HH:mm';
                }
                return 'LT';
            }
            if (shortDate) {
                return 'MM/DD/YYYY';
            }
            // Oct 26, 2017 11:30
            if (clock24Hours) {
                return 'MMM D, YYYY HH:mm';
            }
            // Oct 26, 2017 11:30:30 AM
            if (seconds) {
                return 'll LTS z';
            }
            // Default is Oct 26, 2017 11:30 AM
            return 'lll';
        };
        return _this;
    }
    DateTime.prototype.render = function () {
        var _a;
        var _b = this.props, date = _b.date, utc = _b.utc, _seconds = _b.seconds, _shortDate = _b.shortDate, _dateOnly = _b.dateOnly, _timeOnly = _b.timeOnly, _timeAndDate = _b.timeAndDate, carriedProps = tslib_1.__rest(_b, ["date", "utc", "seconds", "shortDate", "dateOnly", "timeOnly", "timeAndDate"]);
        var user = configStore_1.default.get('user');
        var options = user === null || user === void 0 ? void 0 : user.options;
        var format = this.getFormat(options);
        return (<time {...carriedProps}>
        {utc
                ? moment_1.default.utc(date).format(format)
                : moment_timezone_1.default.tz(date, (_a = options === null || options === void 0 ? void 0 : options.timezone) !== null && _a !== void 0 ? _a : '').format(format)}
      </time>);
    };
    DateTime.defaultProps = {
        seconds: true,
    };
    return DateTime;
}(react_1.Component));
exports.default = DateTime;
//# sourceMappingURL=dateTime.jsx.map