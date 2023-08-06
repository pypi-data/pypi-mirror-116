Object.defineProperty(exports, "__esModule", { value: true });
exports.EventVitalContainer = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var index_1 = require("app/utils/measurements/index");
var constants_1 = require("app/utils/performance/vitals/constants");
function isOutdatedSdk(event) {
    var _a;
    if (!((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.version)) {
        return false;
    }
    var sdkVersion = event.sdk.version;
    return (sdkVersion.startsWith('5.26.') ||
        sdkVersion.startsWith('5.27.0') ||
        sdkVersion.startsWith('5.27.1') ||
        sdkVersion.startsWith('5.27.2'));
}
function EventVitals(_a) {
    var event = _a.event;
    return (<react_1.Fragment>
      <WebVitals event={event}/>
      <MobileVitals event={event}/>
    </react_1.Fragment>);
}
exports.default = EventVitals;
function WebVitals(_a) {
    var _b;
    var event = _a.event;
    var measurementNames = Object.keys((_b = event.measurements) !== null && _b !== void 0 ? _b : {})
        .filter(function (name) { return Boolean(constants_1.WEB_VITAL_DETAILS["measurements." + name]); })
        .sort();
    if (measurementNames.length === 0) {
        return null;
    }
    return (<Container>
      <styles_1.SectionHeading>
        {locale_1.t('Web Vitals')}
        {isOutdatedSdk(event) && (<WarningIconContainer size="sm">
            <tooltip_1.default title={locale_1.t('These vitals were collected using an outdated SDK version and may not be accurate. To ensure accurate web vitals in new transaction events, please update your SDK to the latest version.')} position="top" containerDisplayMode="inline-block">
              <icons_1.IconWarning size="sm"/>
            </tooltip_1.default>
          </WarningIconContainer>)}
      </styles_1.SectionHeading>
      <Measurements>
        {measurementNames.map(function (name) {
            // Measurements are referred to by their full name `measurements.<name>`
            // here but are stored using their abbreviated name `<name>`. Make sure
            // to convert it appropriately.
            var measurement = "measurements." + name;
            var vital = constants_1.WEB_VITAL_DETAILS[measurement];
            return <EventVital key={name} event={event} name={name} vital={vital}/>;
        })}
      </Measurements>
    </Container>);
}
function MobileVitals(_a) {
    var _b;
    var event = _a.event;
    var measurementNames = Object.keys((_b = event.measurements) !== null && _b !== void 0 ? _b : {})
        .filter(function (name) { return Boolean(constants_1.MOBILE_VITAL_DETAILS["measurements." + name]); })
        .sort();
    if (measurementNames.length === 0) {
        return null;
    }
    return (<Container>
      <styles_1.SectionHeading>{locale_1.t('Mobile Vitals')}</styles_1.SectionHeading>
      <Measurements>
        {measurementNames.map(function (name) {
            // Measurements are referred to by their full name `measurements.<name>`
            // here but are stored using their abbreviated name `<name>`. Make sure
            // to convert it appropriately.
            var measurement = "measurements." + name;
            var vital = constants_1.MOBILE_VITAL_DETAILS[measurement];
            return <EventVital key={name} event={event} name={name} vital={vital}/>;
        })}
      </Measurements>
    </Container>);
}
function EventVital(_a) {
    var _b, _c, _d, _e;
    var event = _a.event, name = _a.name, vital = _a.vital;
    var value = (_c = (_b = event.measurements) === null || _b === void 0 ? void 0 : _b[name].value) !== null && _c !== void 0 ? _c : null;
    if (value === null || !vital) {
        return null;
    }
    var failedThreshold = utils_1.defined(vital.poorThreshold) && value >= vital.poorThreshold;
    var currentValue = index_1.formattedValue(vital, value);
    var thresholdValue = index_1.formattedValue(vital, (_d = vital === null || vital === void 0 ? void 0 : vital.poorThreshold) !== null && _d !== void 0 ? _d : 0);
    return (<exports.EventVitalContainer>
      <StyledPanel failedThreshold={failedThreshold}>
        <Name>{(_e = vital.name) !== null && _e !== void 0 ? _e : name}</Name>
        <ValueRow>
          {failedThreshold ? (<FireIconContainer size="sm">
              <tooltip_1.default title={locale_1.t('Fails threshold at %s.', thresholdValue)} position="top" containerDisplayMode="inline-block">
                <icons_1.IconFire size="sm"/>
              </tooltip_1.default>
            </FireIconContainer>) : null}
          <Value failedThreshold={failedThreshold}>{currentValue}</Value>
        </ValueRow>
      </StyledPanel>
    </exports.EventVitalContainer>);
}
var Measurements = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n"])), space_1.default(1));
var Container = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(4));
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  margin-bottom: ", ";\n  ", "\n"], ["\n  padding: ", " ", ";\n  margin-bottom: ", ";\n  ", "\n"])), space_1.default(1), space_1.default(1.5), space_1.default(1), function (p) { return p.failedThreshold && "border: 1px solid " + p.theme.red300 + ";"; });
var Name = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject([""], [""])));
var ValueRow = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var WarningIconContainer = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-left: ", ";\n  color: ", ";\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, space_1.default(0.5), function (p) { return p.theme.red300; });
var FireIconContainer = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-right: ", ";\n  color: ", ";\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-right: ", ";\n  color: ", ";\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, space_1.default(0.5), function (p) { return p.theme.red300; });
var Value = styled_1.default('span')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, function (p) { return p.failedThreshold && "color: " + p.theme.red300 + ";"; });
exports.EventVitalContainer = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=eventVitals.jsx.map