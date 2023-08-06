Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
function FinishSetupAlert(_a) {
    var organization = _a.organization, project = _a.project;
    return (<AlertBar>
      <icons_1.IconLightning />
      <TextWrapper>
        {locale_1.t('You are viewing a sample transaction. Configure performance to start viewing real transactions.')}
      </TextWrapper>
      <button_1.default size="xsmall" priority="primary" target="_blank" external href="https://docs.sentry.io/performance-monitoring/getting-started/" onClick={function () {
            return advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.sample_transaction_docs_link_clicked', {
                project_id: project.id,
                organization: organization,
            });
        }}>
        {locale_1.t('Get Started')}
      </button_1.default>
    </AlertBar>);
}
exports.default = FinishSetupAlert;
var AlertBar = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: ", ";\n  background-color: ", ";\n  padding: 6px 30px;\n  font-size: 14px;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: ", ";\n  background-color: ", ";\n  padding: 6px 30px;\n  font-size: 14px;\n"])), function (p) { return p.theme.headerBackground; }, function (p) { return p.theme.bannerBackground; });
var TextWrapper = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n"], ["\n  margin: 0 ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=finishSetupAlert.jsx.map