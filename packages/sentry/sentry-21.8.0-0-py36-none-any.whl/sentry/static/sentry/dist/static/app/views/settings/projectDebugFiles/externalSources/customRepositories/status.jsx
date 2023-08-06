Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var utils_1 = require("app/components/projects/appStoreConnectContext/utils");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var iconDownload_1 = require("app/icons/iconDownload");
var iconRefresh_1 = require("app/icons/iconRefresh");
var iconWarning_1 = require("app/icons/iconWarning");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Status(_a) {
    var theme = _a.theme, details = _a.details, onEditRepository = _a.onEditRepository, onRevalidateItunesSession = _a.onRevalidateItunesSession;
    var _b = details !== null && details !== void 0 ? details : {}, pendingDownloads = _b.pendingDownloads, updateAlertMessage = _b.updateAlertMessage, itunesSessionValid = _b.itunesSessionValid, appstoreCredentialsValid = _b.appstoreCredentialsValid, lastCheckedBuilds = _b.lastCheckedBuilds;
    if (itunesSessionValid &&
        appstoreCredentialsValid &&
        updateAlertMessage === utils_1.appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt) {
        return (<Wrapper color={theme.red300} onClick={onRevalidateItunesSession}>
        <StyledTooltip title={locale_1.t('We recommend that you revalidate the iTunes session')} containerDisplayMode="inline-flex">
          <iconWarning_1.IconWarning size="sm"/>
        </StyledTooltip>
        {locale_1.t('iTunes session will likely expire soon')}
      </Wrapper>);
    }
    if (itunesSessionValid === false) {
        return (<Wrapper color={theme.red300} onClick={onRevalidateItunesSession}>
        <StyledTooltip title={locale_1.t('Revalidate your iTunes session')} containerDisplayMode="inline-flex">
          <iconWarning_1.IconWarning size="sm"/>
        </StyledTooltip>
        {locale_1.t('iTunes Authentication required')}
      </Wrapper>);
    }
    if (appstoreCredentialsValid === false) {
        return (<Wrapper color={theme.red300} onClick={onEditRepository}>
        <StyledTooltip title={locale_1.t('Recheck your App Store Credentials')} containerDisplayMode="inline-flex">
          <iconWarning_1.IconWarning size="sm"/>
        </StyledTooltip>
        {locale_1.t('Credentials are invalid')}
      </Wrapper>);
    }
    if (pendingDownloads) {
        return (<Wrapper color={theme.gray400}>
        <IconWrapper>
          <iconDownload_1.IconDownload size="sm"/>
        </IconWrapper>
        {locale_1.tn('%s build pending', '%s builds pending', pendingDownloads)}
      </Wrapper>);
    }
    if (lastCheckedBuilds) {
        return (<Wrapper color={theme.gray400}>
        <IconWrapper>
          <iconRefresh_1.IconRefresh size="sm"/>
        </IconWrapper>
        <timeSince_1.default date={lastCheckedBuilds}/>
      </Wrapper>);
    }
    return <placeholder_1.default height="14px"/>;
}
exports.default = react_1.withTheme(Status);
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n  height: 14px;\n  ", ";\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n  height: 14px;\n  ", ";\n"])), space_1.default(0.75), function (p) { return p.color; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.onClick && "cursor: pointer"; });
var StyledTooltip = styled_1.default(tooltip_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: -5px;\n  height: 14px;\n"], ["\n  margin-top: -5px;\n  height: 14px;\n"])));
var IconWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-top: -5px;\n  height: 14px;\n"], ["\n  margin-top: -5px;\n  height: 14px;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=status.jsx.map