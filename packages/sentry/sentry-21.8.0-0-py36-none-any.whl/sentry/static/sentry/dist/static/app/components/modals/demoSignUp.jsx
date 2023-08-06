Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var highlightModalContainer_1 = tslib_1.__importDefault(require("app/components/highlightModalContainer"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var demoMode_1 = require("app/utils/demoMode");
var DemoSignUpModal = function (_a) {
    var closeModal = _a.closeModal;
    var queryParameter = demoMode_1.emailQueryParameter();
    var getStartedExtraParameter = demoMode_1.extraQueryParameter(true);
    var signupUrl = "https://sentry.io/signup/" + queryParameter + getStartedExtraParameter;
    return (<highlightModalContainer_1.default>
      <div>
        <TrialCheckInfo>
          <Subheader>{locale_1.t('Sandbox Signup')}</Subheader>
          <h2>{locale_1.t('Hey, love what you see?')}</h2>
          <p>
            {locale_1.t('Sign up now to setup your own project to see problems within your code and learn how to quickly improve your project.')}
          </p>
        </TrialCheckInfo>
        <StyledButtonBar gap={2}>
          <button_1.default priority="primary" href={signupUrl} onClick={function () {
            return advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.demo_modal_clicked_signup', {
                organization: null,
            });
        }}>
            {locale_1.t('Sign up now')}
          </button_1.default>
          <button_1.default priority="default" onClick={function () {
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.demo_modal_clicked_continue', {
                organization: null,
            });
            closeModal();
        }}>
            {locale_1.t('Keep Exploring')}
          </button_1.default>
        </StyledButtonBar>
      </div>
    </highlightModalContainer_1.default>);
};
var TrialCheckInfo = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " 0;\n  p {\n    font-size: ", ";\n    margin: 0;\n  }\n  h2 {\n    font-size: 1.5em;\n  }\n"], ["\n  padding: ", " 0;\n  p {\n    font-size: ", ";\n    margin: 0;\n  }\n  h2 {\n    font-size: 1.5em;\n  }\n"])), space_1.default(3), function (p) { return p.theme.fontSizeMedium; });
exports.modalCss = react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  max-width: 730px;\n  [role='document'] {\n    position: relative;\n    padding: 70px 80px;\n    overflow: hidden;\n  }\n"], ["\n  width: 100%;\n  max-width: 730px;\n  [role='document'] {\n    position: relative;\n    padding: 70px 80px;\n    overflow: hidden;\n  }\n"])));
var Subheader = styled_1.default('h4')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  text-transform: uppercase;\n  font-weight: bold;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  margin-bottom: ", ";\n  text-transform: uppercase;\n  font-weight: bold;\n  color: ", ";\n  font-size: ", ";\n"])), space_1.default(2), function (p) { return p.theme.purple300; }, function (p) { return p.theme.fontSizeExtraSmall; });
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  max-width: fit-content;\n"], ["\n  margin-top: ", ";\n  max-width: fit-content;\n"])), space_1.default(2));
exports.default = DemoSignUpModal;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=demoSignUp.jsx.map