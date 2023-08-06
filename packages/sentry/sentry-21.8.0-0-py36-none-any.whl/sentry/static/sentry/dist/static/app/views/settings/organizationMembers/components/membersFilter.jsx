Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var getBoolean = function (list) {
    return Array.isArray(list) && list.length
        ? list && list.map(function (v) { return v.toLowerCase(); }).includes('true')
        : null;
};
var MembersFilter = function (_a) {
    var className = _a.className, roles = _a.roles, query = _a.query, onChange = _a.onChange;
    var search = tokenizeSearch_1.tokenizeSearch(query);
    var filters = {
        roles: search.getFilterValues('role') || [],
        isInvited: getBoolean(search.getFilterValues('isInvited')),
        ssoLinked: getBoolean(search.getFilterValues('ssoLinked')),
        has2fa: getBoolean(search.getFilterValues('has2fa')),
    };
    var handleRoleFilter = function (id) { return function () {
        var roleList = new Set(search.getFilterValues('role') ? tslib_1.__spreadArray([], tslib_1.__read(search.getFilterValues('role'))) : []);
        if (roleList.has(id)) {
            roleList.delete(id);
        }
        else {
            roleList.add(id);
        }
        var newSearch = search.copy();
        newSearch.setFilterValues('role', tslib_1.__spreadArray([], tslib_1.__read(roleList)));
        onChange(newSearch.formatString());
    }; };
    var handleBoolFilter = function (key) { return function (value) {
        var newQueryObject = search.copy();
        newQueryObject.removeFilter(key);
        if (value !== null) {
            newQueryObject.setFilterValues(key, [Boolean(value).toString()]);
        }
        onChange(newQueryObject.formatString());
    }; };
    return (<FilterContainer className={className}>
      <FilterHeader>{locale_1.t('Filter By')}</FilterHeader>

      <FilterLists>
        <Filters>
          <h3>{locale_1.t('User Role')}</h3>
          {roles.map(function (_a) {
            var id = _a.id, name = _a.name;
            return (<label key={id}>
              <checkbox_1.default data-test-id={"filter-role-" + id} checked={filters.roles.includes(id)} onChange={handleRoleFilter(id)}/>
              {name}
            </label>);
        })}
        </Filters>

        <Filters>
          <h3>{locale_1.t('Status')}</h3>
          <BooleanFilter data-test-id="filter-isInvited" onChange={handleBoolFilter('isInvited')} value={filters.isInvited}>
            {locale_1.t('Invited')}
          </BooleanFilter>
          <BooleanFilter data-test-id="filter-has2fa" onChange={handleBoolFilter('has2fa')} value={filters.has2fa}>
            {locale_1.t('2FA')}
          </BooleanFilter>
          <BooleanFilter data-test-id="filter-ssoLinked" onChange={handleBoolFilter('ssoLinked')} value={filters.ssoLinked}>
            {locale_1.t('SSO Linked')}
          </BooleanFilter>
        </Filters>
      </FilterLists>
    </FilterContainer>);
};
var BooleanFilter = function (_a) {
    var onChange = _a.onChange, value = _a.value, children = _a.children;
    return (<label>
    <checkbox_1.default checked={value !== null} onChange={function () { return onChange(value === null ? true : null); }}/>
    {children}
    <switchButton_1.default isDisabled={value === null} isActive={value === true} toggle={function () { return onChange(!value); }}/>
  </label>);
};
var FilterContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-radius: 4px;\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n"], ["\n  border-radius: 4px;\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; });
var FilterHeader = styled_1.default('h2')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-top-left-radius: 4px;\n  border-top-right-radius: 4px;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  font-size: ", ";\n  padding: ", ";\n  margin: 0;\n"], ["\n  border-top-left-radius: 4px;\n  border-top-right-radius: 4px;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  font-size: ", ";\n  padding: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(1));
var FilterLists = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 100px max-content;\n  grid-gap: ", ";\n  margin: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 100px max-content;\n  grid-gap: ", ";\n  margin: ", ";\n  margin-top: ", ";\n"])), space_1.default(3), space_1.default(1.5), space_1.default(0.75));
var Filters = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(auto-fit, minmax(0, max-content));\n  grid-gap: ", ";\n  font-size: ", ";\n\n  h3 {\n    color: #000;\n    font-size: ", ";\n    text-transform: uppercase;\n    margin: ", " 0;\n  }\n\n  label {\n    display: grid;\n    grid-template-columns: max-content 1fr max-content;\n    grid-gap: ", ";\n    align-items: center;\n    font-weight: normal;\n    white-space: nowrap;\n    height: ", ";\n  }\n\n  input,\n  label {\n    margin: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-rows: repeat(auto-fit, minmax(0, max-content));\n  grid-gap: ", ";\n  font-size: ", ";\n\n  h3 {\n    color: #000;\n    font-size: ", ";\n    text-transform: uppercase;\n    margin: ", " 0;\n  }\n\n  label {\n    display: grid;\n    grid-template-columns: max-content 1fr max-content;\n    grid-gap: ", ";\n    align-items: center;\n    font-weight: normal;\n    white-space: nowrap;\n    height: ", ";\n  }\n\n  input,\n  label {\n    margin: 0;\n  }\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.fontSizeSmall; }, space_1.default(1), space_1.default(0.75), space_1.default(2));
exports.default = MembersFilter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=membersFilter.jsx.map