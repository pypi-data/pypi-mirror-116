Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_autosize_textarea_1 = tslib_1.__importDefault(require("react-autosize-textarea"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var input_1 = require("app/styles/input");
var utils_1 = require("app/utils");
var ruleBuilder_1 = tslib_1.__importDefault(require("./ruleBuilder"));
var defaultProps = {
    urls: [],
    paths: [],
    disabled: false,
};
var OwnerInput = /** @class */ (function (_super) {
    tslib_1.__extends(OwnerInput, _super);
    function OwnerInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasChanges: false,
            text: null,
            error: null,
        };
        _this.handleUpdateOwnership = function () {
            var _a = _this.props, organization = _a.organization, project = _a.project, onSave = _a.onSave;
            var text = _this.state.text;
            _this.setState({ error: null });
            var api = new api_1.Client();
            var request = api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/ownership/", {
                method: 'PUT',
                data: { raw: text || '' },
            });
            request
                .then(function () {
                indicator_1.addSuccessMessage(locale_1.t('Updated issue ownership rules'));
                _this.setState({
                    hasChanges: false,
                    text: text,
                }, function () { return onSave && onSave(text); });
            })
                .catch(function (error) {
                _this.setState({ error: error.responseJSON });
                if (error.status === 403) {
                    indicator_1.addErrorMessage(locale_1.t("You don't have permission to modify issue ownership rules for this project"));
                }
                else if (error.status === 400 &&
                    error.responseJSON.raw &&
                    error.responseJSON.raw[0].startsWith('Invalid rule owners:')) {
                    indicator_1.addErrorMessage(locale_1.t('Unable to save issue ownership rule changes: ' + error.responseJSON.raw[0]));
                }
                else {
                    indicator_1.addErrorMessage(locale_1.t('Unable to save issue ownership rule changes'));
                }
            });
            return request;
        };
        _this.handleChange = function (e) {
            _this.setState({
                hasChanges: true,
                text: e.target.value,
            });
        };
        _this.handleAddRule = function (rule) {
            var initialText = _this.props.initialText;
            _this.setState(function (_a) {
                var text = _a.text;
                return ({
                    text: (text || initialText) + '\n' + rule,
                });
            }, _this.handleUpdateOwnership);
        };
        return _this;
    }
    OwnerInput.prototype.parseError = function (error) {
        var _a, _b, _c;
        var text = (_a = error === null || error === void 0 ? void 0 : error.raw) === null || _a === void 0 ? void 0 : _a[0];
        if (!text) {
            return null;
        }
        if (text.startsWith('Invalid rule owners:')) {
            return <InvalidOwners>{text}</InvalidOwners>;
        }
        else {
            return (<SyntaxOverlay line={parseInt((_c = (_b = text.match(/line (\d*),/)) === null || _b === void 0 ? void 0 : _b[1]) !== null && _c !== void 0 ? _c : '', 10) - 1}/>);
        }
    };
    OwnerInput.prototype.mentionableUsers = function () {
        return memberListStore_1.default.getAll().map(function (member) { return ({
            id: member.id,
            display: member.email,
            email: member.email,
        }); });
    };
    OwnerInput.prototype.mentionableTeams = function () {
        var project = this.props.project;
        var projectWithTeams = projectsStore_1.default.getBySlug(project.slug);
        if (!projectWithTeams) {
            return [];
        }
        return projectWithTeams.teams.map(function (team) { return ({
            id: team.id,
            display: "#" + team.slug,
            email: team.id,
        }); });
    };
    OwnerInput.prototype.render = function () {
        var _this = this;
        var _a = this.props, project = _a.project, organization = _a.organization, disabled = _a.disabled, urls = _a.urls, paths = _a.paths, initialText = _a.initialText;
        var _b = this.state, hasChanges = _b.hasChanges, text = _b.text, error = _b.error;
        return (<React.Fragment>
        <ruleBuilder_1.default urls={urls} paths={paths} organization={organization} project={project} onAddRule={this.handleAddRule.bind(this)} disabled={disabled}/>
        <div style={{ position: 'relative' }} onKeyDown={function (e) {
                if (e.metaKey && e.key === 'Enter') {
                    _this.handleUpdateOwnership();
                }
            }}>
          <StyledTextArea placeholder={'#example usage\n' +
                'path:src/example/pipeline/* person@sentry.io #infra\n' +
                'url:http://example.com/settings/* #product\n' +
                'tags.sku_class:enterprise #enterprise'} onChange={this.handleChange} disabled={disabled} value={utils_1.defined(text) ? text : initialText} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off"/>
          <ActionBar>
            <div>{this.parseError(error)}</div>
            <SaveButton>
              <button_1.default size="small" priority="primary" onClick={this.handleUpdateOwnership} disabled={disabled || !hasChanges}>
                {locale_1.t('Save Changes')}
              </button_1.default>
            </SaveButton>
          </ActionBar>
        </div>
      </React.Fragment>);
    };
    OwnerInput.defaultProps = defaultProps;
    return OwnerInput;
}(React.Component));
var TEXTAREA_PADDING = 4;
var TEXTAREA_LINE_HEIGHT = 24;
var ActionBar = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var SyntaxOverlay = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n  width: 100%;\n  height: ", "px;\n  background-color: red;\n  opacity: 0.1;\n  pointer-events: none;\n  position: absolute;\n  top: ", "px;\n"], ["\n  ", ";\n  width: 100%;\n  height: ", "px;\n  background-color: red;\n  opacity: 0.1;\n  pointer-events: none;\n  position: absolute;\n  top: ", "px;\n"])), input_1.inputStyles, TEXTAREA_LINE_HEIGHT, function (_a) {
    var line = _a.line;
    return TEXTAREA_PADDING + line * 24;
});
var SaveButton = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: end;\n  padding-top: 10px;\n"], ["\n  text-align: end;\n  padding-top: 10px;\n"])));
var StyledTextArea = styled_1.default(react_autosize_textarea_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n  min-height: 140px;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  padding-top: ", "px;\n  line-height: ", "px;\n"], ["\n  ", ";\n  min-height: 140px;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  padding-top: ", "px;\n  line-height: ", "px;\n"])), function (p) { return input_1.inputStyles(p); }, function (p) { return p.theme.text.familyMono; }, TEXTAREA_PADDING, TEXTAREA_LINE_HEIGHT);
var InvalidOwners = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: bold;\n  margin-top: 12px;\n"], ["\n  color: ", ";\n  font-weight: bold;\n  margin-top: 12px;\n"])), function (p) { return p.theme.error; });
exports.default = OwnerInput;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=ownerInput.jsx.map