Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var debugFiles_1 = require("app/types/debugFiles");
var actions_1 = tslib_1.__importDefault(require("./actions"));
var details_1 = tslib_1.__importDefault(require("./details"));
var status_1 = tslib_1.__importDefault(require("./status"));
var utils_1 = require("./utils");
function Repository(_a) {
    var repository = _a.repository, onDelete = _a.onDelete, onEdit = _a.onEdit;
    var _b = tslib_1.__read(react_1.useState(false), 2), isDetailsExpanded = _b[0], setIsDetailsExpanded = _b[1];
    var id = repository.id, name = repository.name, type = repository.type;
    return (<StyledPanelItem>
      <Name>{name}</Name>
      <TypeAndStatus>
        {utils_1.customRepoTypeLabel[type]}
        {repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT && (<status_1.default details={repository.details} onEditRepository={function () { return onEdit(id); }} onRevalidateItunesSession={function () { return onEdit(id, true); }}/>)}
      </TypeAndStatus>
      <actions_1.default repositoryName={name} onDelete={function () { return onDelete(id); }} onEdit={function () { return onEdit(id); }} showDetails={repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT} isDetailsDisabled={repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT &&
            repository.details === undefined} isDetailsExpanded={isDetailsExpanded} onToggleDetails={function () { return setIsDetailsExpanded(!isDetailsExpanded); }}/>
      {repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT && isDetailsExpanded && (<details_1.default details={repository.details}/>)}
    </StyledPanelItem>);
}
exports.default = Repository;
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  row-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n    grid-template-rows: repeat(2, max-content);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  row-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n    grid-template-rows: repeat(2, max-content);\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[0]; });
var Name = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    grid-row: 1 / 2;\n  }\n"], ["\n  @media (min-width: ", ") {\n    grid-row: 1 / 2;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var TypeAndStatus = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  align-items: center;\n\n  @media (min-width: ", ") {\n    grid-template-columns: max-content minmax(200px, max-content);\n    grid-row: 2 / 3;\n    grid-gap: ", ";\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  align-items: center;\n\n  @media (min-width: ", ") {\n    grid-template-columns: max-content minmax(200px, max-content);\n    grid-row: 2 / 3;\n    grid-gap: ", ";\n  }\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1.5), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=repository.jsx.map