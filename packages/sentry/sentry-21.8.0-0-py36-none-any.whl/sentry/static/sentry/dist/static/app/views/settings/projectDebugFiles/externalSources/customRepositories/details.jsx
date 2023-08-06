Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Details(_a) {
    var details = _a.details;
    var _b = details !== null && details !== void 0 ? details : {}, latestBuildVersion = _b.latestBuildVersion, latestBuildNumber = _b.latestBuildNumber, lastCheckedBuilds = _b.lastCheckedBuilds;
    return (<Wrapper>
      {locale_1.t('Last detected version')}
      <Value>
        {latestBuildVersion ? (locale_1.tct('v[version]', { version: latestBuildVersion })) : (<notAvailable_1.default tooltip={locale_1.t('Not available')}/>)}
      </Value>

      {locale_1.t('Last detected build')}
      <Value>{latestBuildNumber !== null && latestBuildNumber !== void 0 ? latestBuildNumber : <notAvailable_1.default tooltip={locale_1.t('Not available')}/>}</Value>

      {locale_1.t('Detected last build on')}
      <Value>
        {lastCheckedBuilds ? (<dateTime_1.default date={lastCheckedBuilds}/>) : (<notAvailable_1.default tooltip={locale_1.t('Not available')}/>)}
      </Value>
    </Wrapper>);
}
exports.default = Details;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  margin-top: ", ";\n  align-items: center;\n\n  font-size: ", ";\n  font-weight: 700;\n\n  @media (min-width: ", ") {\n    margin-top: ", ";\n    grid-template-columns: max-content 1fr;\n    grid-gap: ", ";\n    grid-row: 3/3;\n    grid-column: 1/-1;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  margin-top: ", ";\n  align-items: center;\n\n  font-size: ", ";\n  font-weight: 700;\n\n  @media (min-width: ", ") {\n    margin-top: ", ";\n    grid-template-columns: max-content 1fr;\n    grid-gap: ", ";\n    grid-row: 3/3;\n    grid-column: 1/-1;\n  }\n"])), space_1.default(1), space_1.default(0.5), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(1), space_1.default(1));
var Value = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 400;\n  white-space: pre-wrap;\n  word-break: break-all;\n  padding: ", " ", ";\n  font-family: ", ";\n  background-color: ", ";\n\n  @media (max-width: ", ") {\n    :not(:last-child) {\n      margin-bottom: ", ";\n    }\n  }\n"], ["\n  font-weight: 400;\n  white-space: pre-wrap;\n  word-break: break-all;\n  padding: ", " ", ";\n  font-family: ", ";\n  background-color: ", ";\n\n  @media (max-width: ", ") {\n    :not(:last-child) {\n      margin-bottom: ", ";\n    }\n  }\n"])), space_1.default(1), space_1.default(1.5), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=details.jsx.map