Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
function ErrorMessage(_a) {
    var _b;
    var error = _a.error, groupId = _a.groupId, onRetry = _a.onRetry, orgSlug = _a.orgSlug, projSlug = _a.projSlug;
    function getErrorDetails(errorCode) {
        switch (errorCode) {
            case 'merged_issues':
                return {
                    title: locale_1.t('Grouping breakdown is not available in this issue'),
                    subTitle: locale_1.t('This issue needs to be fully unmerged before grouping breakdown is available'),
                    action: (<button_1.default priority="primary" to={"/organizations/sentry/issues/" + groupId + "/merged/?" + location.search}>
              {locale_1.t('Unmerge issue')}
            </button_1.default>),
                };
            case 'missing_feature':
                return {
                    title: locale_1.t('This project does not have the grouping breakdown available. Is your organization still an early adopter?'),
                };
            case 'no_events':
                return {
                    title: locale_1.t('This issue has no events'),
                };
            case 'issue_not_hierarchical':
                return {
                    title: locale_1.t('Grouping breakdown is not available in this issue'),
                    subTitle: locale_1.t('Only new issues with the latest grouping strategy have this feature available'),
                };
            case 'project_not_hierarchical':
                return {
                    title: locale_1.t('Update your Grouping Config'),
                    subTitle: (<react_1.default.Fragment>
              <p>
                {locale_1.t('Enable advanced grouping insights and functionality by updating this project to the latest Grouping Config:')}
              </p>

              <ul>
                <li>
                  {locale_1.tct('[strong:Breakdowns:] Explore events in this issue by call hierarchy.', { strong: <strong /> })}
                </li>
                <li>
                  {locale_1.tct('[strong:Stack trace annotations:] See important frames Sentry uses to group issues directly in the stack trace.', { strong: <strong /> })}
                </li>
              </ul>
            </react_1.default.Fragment>),
                    leftAligned: true,
                    action: (<buttonBar_1.default gap={1}>
              <button_1.default priority="primary" to={"/settings/" + orgSlug + "/projects/" + projSlug + "/issue-grouping/#upgrade-grouping"}>
                {locale_1.t('Upgrade Grouping Config')}
              </button_1.default>
              <button_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/grouping-breakdown/">
                {locale_1.t('Read the docs')}
              </button_1.default>
            </buttonBar_1.default>),
                };
            default:
                return {};
        }
    }
    if (typeof error === 'string') {
        return <alert_1.default type="warning">{error}</alert_1.default>;
    }
    if (error.status === 403 && ((_b = error.responseJSON) === null || _b === void 0 ? void 0 : _b.detail)) {
        var _c = error.responseJSON.detail, code = _c.code, message = _c.message;
        var _d = getErrorDetails(code), action = _d.action, title = _d.title, subTitle = _d.subTitle, leftAligned = _d.leftAligned;
        return (<panels_1.Panel>
        <emptyMessage_1.default size="large" title={title !== null && title !== void 0 ? title : message} description={subTitle} action={action} leftAligned={leftAligned}/>
      </panels_1.Panel>);
    }
    return (<loadingError_1.default message={locale_1.t('Unable to load grouping levels, please try again later')} onRetry={onRetry}/>);
}
exports.default = ErrorMessage;
//# sourceMappingURL=errorMessage.jsx.map