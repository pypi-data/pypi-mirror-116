Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_autosize_textarea_1 = tslib_1.__importDefault(require("react-autosize-textarea"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RulesPanel = /** @class */ (function (_super) {
    tslib_1.__extends(RulesPanel, _super);
    function RulesPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RulesPanel.prototype.renderIcon = function (provider) {
        switch (provider) {
            case 'github':
                return <icons_1.IconGithub size="md"/>;
            case 'gitlab':
                return <icons_1.IconGitlab size="md"/>;
            default:
                return <icons_1.IconSentry size="md"/>;
        }
    };
    RulesPanel.prototype.renderTitle = function () {
        switch (this.props.type) {
            case 'codeowners':
                return 'CODEOWNERS';
            case 'issueowners':
                return 'Ownership Rules';
            default:
                return null;
        }
    };
    RulesPanel.prototype.render = function () {
        var _a = this.props, raw = _a.raw, dateUpdated = _a.dateUpdated, provider = _a.provider, repoName = _a.repoName, placeholder = _a.placeholder, controls = _a.controls, beta = _a.beta, dataTestId = _a["data-test-id"];
        return (<panels_1.Panel data-test-id={dataTestId}>
        <panels_1.PanelHeader>
          {[
                <Container key="title">
              {this.renderIcon(provider !== null && provider !== void 0 ? provider : '')}
              <Title>{this.renderTitle()}</Title>
              {repoName && <Repository>{"- " + repoName}</Repository>}
              {beta && <featureBadge_1.default type="beta"/>}
            </Container>,
                <Container key="control">
              <SyncDate>
                {dateUpdated && "Last synced " + moment_1.default(dateUpdated).fromNow()}
              </SyncDate>
              <Controls>
                {(controls || []).map(function (c, n) { return (<span key={n}> {c}</span>); })}
              </Controls>
            </Container>,
            ]}
        </panels_1.PanelHeader>

        <panels_1.PanelBody>
          <InnerPanelBody>
            <StyledTextArea value={raw} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off" placeholder={placeholder}/>
          </InnerPanelBody>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return RulesPanel;
}(React.Component));
exports.default = react_1.withTheme(RulesPanel);
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  text-transform: none;\n"], ["\n  display: flex;\n  align-items: center;\n  text-transform: none;\n"])));
var Title = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: 0 ", " 0 ", ";\n  font-size: initial;\n"], ["\n  padding: 0 ", " 0 ", ";\n  font-size: initial;\n"])), space_1.default(0.5), space_1.default(1));
var Repository = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
var InnerPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  height: auto;\n"], ["\n  height: auto;\n"])));
var StyledTextArea = styled_1.default(react_autosize_textarea_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n  height: 350px !important;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  line-height: ", ";\n  border: none;\n  box-shadow: none;\n  padding: ", ";\n  color: transparent;\n  text-shadow: 0 0 0 #9386a0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border: none;\n    box-shadow: none;\n  }\n"], ["\n  ", ";\n  height: 350px !important;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  line-height: ", ";\n  border: none;\n  box-shadow: none;\n  padding: ", ";\n  color: transparent;\n  text-shadow: 0 0 0 #9386a0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border: none;\n    box-shadow: none;\n  }\n"])), function (p) { return input_1.inputStyles(p); }, function (p) { return p.theme.text.familyMono; }, space_1.default(3), space_1.default(2));
var SyncDate = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding: 0 ", ";\n  font-weight: normal;\n"], ["\n  padding: 0 ", ";\n  font-weight: normal;\n"])), space_1.default(1));
var Controls = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n"], ["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=rulesPanel.jsx.map