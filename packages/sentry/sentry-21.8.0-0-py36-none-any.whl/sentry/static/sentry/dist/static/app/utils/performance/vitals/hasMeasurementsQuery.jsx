Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var utils_1 = require("app/utils");
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function getHasMeasurementsRequestPayload(props) {
    var eventView = props.eventView, location = props.location, transaction = props.transaction, type = props.type;
    var escaped = utils_1.escapeDoubleQuotes(tokenizeSearch_1.escapeFilterValue(transaction));
    var baseApiPayload = {
        transaction: "\"" + escaped + "\"",
        type: type,
    };
    var additionalApiPayload = pick_1.default(eventView.getEventsAPIPayload(location), [
        'project',
        'environment',
    ]);
    return Object.assign(baseApiPayload, additionalApiPayload);
}
function beforeFetch(api) {
    api.clear();
}
function HasMeasurementsQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-has-measurements" getRequestPayload={getHasMeasurementsRequestPayload} beforeFetch={beforeFetch} {...omit_1.default(props, 'children')}>
      {function (_a) {
            var _b;
            var tableData = _a.tableData, rest = tslib_1.__rest(_a, ["tableData"]);
            return props.children(tslib_1.__assign({ hasMeasurements: (_b = tableData === null || tableData === void 0 ? void 0 : tableData.measurements) !== null && _b !== void 0 ? _b : null }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = withApi_1.default(HasMeasurementsQuery);
//# sourceMappingURL=hasMeasurementsQuery.jsx.map