Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var displayOptions_1 = tslib_1.__importDefault(require("./displayOptions"));
var searchBar_1 = tslib_1.__importDefault(require("./searchBar"));
var sortOptions_1 = tslib_1.__importDefault(require("./sortOptions"));
var IssueListFilters = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListFilters, _super);
    function IssueListFilters() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IssueListFilters.prototype.render = function () {
        var _a = this.props, organization = _a.organization, savedSearch = _a.savedSearch, query = _a.query, isSearchDisabled = _a.isSearchDisabled, sort = _a.sort, display = _a.display, hasSessions = _a.hasSessions, selectedProjects = _a.selectedProjects, onSidebarToggle = _a.onSidebarToggle, onSearch = _a.onSearch, onSortChange = _a.onSortChange, onDisplayChange = _a.onDisplayChange, tagValueLoader = _a.tagValueLoader, tags = _a.tags;
        var isAssignedQuery = /\bassigned:/.test(query);
        var hasIssuePercentDisplay = organization.features.includes('issue-percent-display');
        return (<SearchContainer hasIssuePercentDisplay={hasIssuePercentDisplay}>
        <react_1.ClassNames>
          {function (_a) {
                var css = _a.css;
                return (<guideAnchor_1.default target="assigned_or_suggested_query" disabled={!isAssignedQuery} containerClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                width: 100%;\n              "], ["\n                width: 100%;\n              "])))}>
              <searchBar_1.default organization={organization} query={query || ''} sort={sort} onSearch={onSearch} disabled={isSearchDisabled} excludeEnvironment supportedTags={tags} tagValueLoader={tagValueLoader} savedSearch={savedSearch} onSidebarToggle={onSidebarToggle}/>
            </guideAnchor_1.default>);
            }}
        </react_1.ClassNames>

        <DropdownsWrapper hasIssuePercentDisplay={hasIssuePercentDisplay}>
          {hasIssuePercentDisplay && (<displayOptions_1.default onDisplayChange={onDisplayChange} display={display} hasSessions={hasSessions} hasMultipleProjectsSelected={selectedProjects.length !== 1 || selectedProjects[0] === -1}/>)}
          <sortOptions_1.default sort={sort} query={query} onSelect={onSortChange}/>
        </DropdownsWrapper>
      </SearchContainer>);
    };
    return IssueListFilters;
}(React.Component));
var SearchContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr auto;\n  }\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n  }\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr auto;\n  }\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n  }\n"])), space_1.default(1), space_1.default(2), function (p) { return p.theme.breakpoints[p.hasIssuePercentDisplay ? 1 : 0]; }, function (p) { return p.theme.breakpoints[0]; });
var DropdownsWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n  }\n"])), space_1.default(1), function (p) { return (p.hasIssuePercentDisplay ? '1fr' : ''); }, function (p) { return p.theme.breakpoints[0]; });
exports.default = IssueListFilters;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=filters.jsx.map