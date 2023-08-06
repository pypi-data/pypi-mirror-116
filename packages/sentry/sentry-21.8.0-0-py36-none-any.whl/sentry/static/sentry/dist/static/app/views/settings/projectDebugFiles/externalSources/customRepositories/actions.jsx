Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var button_2 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirmDelete_1 = tslib_1.__importDefault(require("app/components/confirmDelete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var iconEllipsis_1 = require("app/icons/iconEllipsis");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
function Actions(_a) {
    var repositoryName = _a.repositoryName, isDetailsExpanded = _a.isDetailsExpanded, isDetailsDisabled = _a.isDetailsDisabled, onToggleDetails = _a.onToggleDetails, onEdit = _a.onEdit, onDelete = _a.onDelete, showDetails = _a.showDetails;
    function renderConfirmDelete(element) {
        return (<confirmDelete_1.default confirmText={locale_1.t('Delete Repository')} message={<react_1.Fragment>
            <textBlock_1.default>
              <strong>
                {locale_1.t('Removing this repository applies instantly to new events.')}
              </strong>
            </textBlock_1.default>
            <textBlock_1.default>
              {locale_1.t('Debug files from this repository will not be used to symbolicate future events. This may create new issues and alert members in your organization.')}
            </textBlock_1.default>
          </react_1.Fragment>} confirmInput={repositoryName} priority="danger" onConfirm={onDelete}>
        {element}
      </confirmDelete_1.default>);
    }
    return (<StyledButtonBar gap={1}>
      {showDetails && (<StyledDropdownButton isOpen={isDetailsExpanded} size="small" onClick={onToggleDetails} hideBottomBorder={false} disabled={isDetailsDisabled}>
          {locale_1.t('Details')}
        </StyledDropdownButton>)}
      <StyledButton onClick={onEdit} size="small">
        {locale_1.t('Configure')}
      </StyledButton>
      {renderConfirmDelete(<StyledButton size="small">{locale_1.t('Delete')}</StyledButton>)}
      <DropDownWrapper>
        <dropdownLink_1.default caret={false} customTitle={<StyledActionButton label={locale_1.t('Actions')} icon={<iconEllipsis_1.IconEllipsis />}/>} anchorRight>
          <menuItemActionLink_1.default title={locale_1.t('Configure')} onClick={onEdit}>
            {locale_1.t('Configure')}
          </menuItemActionLink_1.default>
          {renderConfirmDelete(<menuItemActionLink_1.default title={locale_1.t('Delete')}>{locale_1.t('Delete')}</menuItemActionLink_1.default>)}
        </dropdownLink_1.default>
      </DropDownWrapper>
    </StyledButtonBar>);
}
exports.default = Actions;
var StyledActionButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 32px;\n"], ["\n  height: 32px;\n"])));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-bottom-right-radius: ", ";\n  border-bottom-left-radius: ", ";\n"], ["\n  border-bottom-right-radius: ", ";\n  border-bottom-left-radius: ", ";\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    grid-row: 1 / 3;\n  }\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-gap: ", ";\n    margin-top: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    grid-row: 1 / 3;\n  }\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-gap: ", ";\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(1), space_1.default(0.5));
var StyledButton = styled_1.default(button_2.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var DropDownWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=actions.jsx.map