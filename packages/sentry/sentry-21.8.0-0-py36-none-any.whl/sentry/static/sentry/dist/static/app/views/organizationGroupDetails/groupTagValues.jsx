Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var dataExport_1 = tslib_1.__importStar(require("app/components/dataExport"));
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var userBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/userBadge"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var DEFAULT_SORT = 'count';
var GroupTagValues = /** @class */ (function (_super) {
    tslib_1.__extends(GroupTagValues, _super);
    function GroupTagValues() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupTagValues.prototype.getEndpoints = function () {
        var environment = this.props.environments;
        var _a = this.props.params, groupId = _a.groupId, tagKey = _a.tagKey;
        return [
            ['tag', "/issues/" + groupId + "/tags/" + tagKey + "/"],
            [
                'tagValueList',
                "/issues/" + groupId + "/tags/" + tagKey + "/values/",
                { query: { environment: environment, sort: this.getSort() } },
            ],
        ];
    };
    GroupTagValues.prototype.getSort = function () {
        return this.props.location.query.sort || DEFAULT_SORT;
    };
    GroupTagValues.prototype.renderLoading = function () {
        return this.renderBody();
    };
    GroupTagValues.prototype.renderResults = function () {
        var _a = this.props, baseUrl = _a.baseUrl, project = _a.project, environment = _a.environments, _b = _a.params, orgId = _b.orgId, groupId = _b.groupId, tagKey = _b.tagKey;
        var _c = this.state, tagValueList = _c.tagValueList, tag = _c.tag;
        var discoverFields = [
            'title',
            'release',
            'environment',
            'user.display',
            'timestamp',
        ];
        return tagValueList === null || tagValueList === void 0 ? void 0 : tagValueList.map(function (tagValue, tagValueIdx) {
            var _a, _b;
            var pct = (tag === null || tag === void 0 ? void 0 : tag.totalValues)
                ? utils_1.percent(tagValue.count, tag === null || tag === void 0 ? void 0 : tag.totalValues).toFixed(2) + "%"
                : '--';
            var key = (_a = tagValue.key) !== null && _a !== void 0 ? _a : tagKey;
            var issuesQuery = tagValue.query || key + ":\"" + tagValue.value + "\"";
            var discoverView = eventView_1.default.fromSavedQuery({
                id: undefined,
                name: key,
                fields: tslib_1.__spreadArray([key], tslib_1.__read(discoverFields.filter(function (field) { return field !== key; }))),
                orderby: '-timestamp',
                query: "issue.id:" + groupId + " " + issuesQuery,
                projects: [Number(project === null || project === void 0 ? void 0 : project.id)],
                environment: environment,
                version: 2,
                range: '90d',
            });
            var issuesPath = "/organizations/" + orgId + "/issues/";
            return (<react_1.Fragment key={tagValueIdx}>
          <NameColumn>
            <NameWrapper data-test-id="group-tag-value">
              <globalSelectionLink_1.default to={{
                    pathname: baseUrl + "events/",
                    query: { query: issuesQuery },
                }}>
                {key === 'user' ? (<userBadge_1.default user={tslib_1.__assign(tslib_1.__assign({}, tagValue), { id: (_b = tagValue.identifier) !== null && _b !== void 0 ? _b : '' })} avatarSize={20} hideEmail/>) : (<deviceName_1.default value={tagValue.name}/>)}
              </globalSelectionLink_1.default>
            </NameWrapper>

            {tagValue.email && (<StyledExternalLink href={"mailto:" + tagValue.email} data-test-id="group-tag-mail">
                <icons_1.IconMail size="xs" color="gray300"/>
              </StyledExternalLink>)}
            {utils_1.isUrl(tagValue.value) && (<StyledExternalLink href={tagValue.value} data-test-id="group-tag-url">
                <icons_1.IconOpen size="xs" color="gray300"/>
              </StyledExternalLink>)}
          </NameColumn>
          <RightAlignColumn>{pct}</RightAlignColumn>
          <RightAlignColumn>{tagValue.count.toLocaleString()}</RightAlignColumn>
          <RightAlignColumn>
            <timeSince_1.default date={tagValue.lastSeen}/>
          </RightAlignColumn>
          <RightAlignColumn>
            <dropdownLink_1.default anchorRight alwaysRenderMenu={false} caret={false} title={<button_1.default tooltipProps={{
                        containerDisplayMode: 'flex',
                    }} size="small" type="button" aria-label={locale_1.t('Show more')} icon={<icons_1.IconEllipsis size="xs"/>}/>}>
              <feature_1.default features={['organizations:discover-basic']}>
                <li>
                  <react_router_1.Link to={discoverView.getResultsViewUrlTarget(orgId)}>
                    {locale_1.t('Open in Discover')}
                  </react_router_1.Link>
                </li>
              </feature_1.default>
              <li>
                <globalSelectionLink_1.default to={{ pathname: issuesPath, query: { query: issuesQuery } }}>
                  {locale_1.t('Search All Issues with Tag Value')}
                </globalSelectionLink_1.default>
              </li>
            </dropdownLink_1.default>
          </RightAlignColumn>
        </react_1.Fragment>);
        });
    };
    GroupTagValues.prototype.renderBody = function () {
        var _a = this.props, group = _a.group, _b = _a.params, orgId = _b.orgId, tagKey = _b.tagKey, query = _a.location.query, environments = _a.environments;
        var _c = this.state, tagValueList = _c.tagValueList, tag = _c.tag, tagValueListPageLinks = _c.tagValueListPageLinks, loading = _c.loading;
        var _cursor = query.cursor, _page = query.page, currentQuery = tslib_1.__rest(query, ["cursor", "page"]);
        var title = tagKey === 'user' ? locale_1.t('Affected Users') : tagKey;
        var sort = this.getSort();
        var sortArrow = <icons_1.IconArrow color="gray300" size="xs" direction="down"/>;
        var lastSeenColumnHeader = (<StyledSortLink to={{
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { sort: 'date' }),
            }}>
        {locale_1.t('Last Seen')} {sort === 'date' && sortArrow}
      </StyledSortLink>);
        var countColumnHeader = (<StyledSortLink to={{
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { sort: 'count' }),
            }}>
        {locale_1.t('Count')} {sort === 'count' && sortArrow}
      </StyledSortLink>);
        return (<react_1.Fragment>
        <TitleWrapper>
          <Title>{locale_1.t('Tag Details')}</Title>
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" priority="default" href={"/" + orgId + "/" + group.project.slug + "/issues/" + group.id + "/tags/" + tagKey + "/export/"}>
              {locale_1.t('Export Page to CSV')}
            </button_1.default>
            <dataExport_1.default payload={{
                queryType: dataExport_1.ExportQueryType.IssuesByTag,
                queryInfo: {
                    project: group.project.id,
                    group: group.id,
                    key: tagKey,
                },
            }}/>
          </buttonBar_1.default>
        </TitleWrapper>
        <StyledPanelTable isLoading={loading} isEmpty={(tagValueList === null || tagValueList === void 0 ? void 0 : tagValueList.length) === 0} headers={[
                title,
                <PercentColumnHeader key="percent">{locale_1.t('Percent')}</PercentColumnHeader>,
                countColumnHeader,
                lastSeenColumnHeader,
                '',
            ]} emptyMessage={locale_1.t('Sorry, the tags for this issue could not be found.')} emptyAction={!!(environments === null || environments === void 0 ? void 0 : environments.length)
                ? locale_1.t('No tags were found for the currently selected environments')
                : null}>
          {tagValueList && tag && this.renderResults()}
        </StyledPanelTable>
        <StyledPagination pageLinks={tagValueListPageLinks}/>
      </react_1.Fragment>);
    };
    return GroupTagValues;
}(asyncComponent_1.default));
exports.default = GroupTagValues;
var TitleWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  flex-wrap: wrap;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  flex-wrap: wrap;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var Title = styled_1.default('h3')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  font-size: ", ";\n\n  overflow: auto;\n  @media (min-width: ", ") {\n    overflow: initial;\n  }\n\n  & > * {\n    padding: ", " ", ";\n  }\n"], ["\n  white-space: nowrap;\n  font-size: ", ";\n\n  overflow: auto;\n  @media (min-width: ", ") {\n    overflow: initial;\n  }\n\n  & > * {\n    padding: ", " ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(1), space_1.default(2));
var PercentColumnHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var StyledSortLink = styled_1.default(react_router_1.Link)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"], ["\n  text-align: right;\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"])));
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
var Column = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var NameColumn = styled_1.default(Column)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  ", ";\n  display: flex;\n  min-width: 320px;\n"], ["\n  ", ";\n  display: flex;\n  min-width: 320px;\n"])), overflowEllipsis_1.default);
var NameWrapper = styled_1.default('span')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  ", ";\n  width: auto;\n"], ["\n  ", ";\n  width: auto;\n"])), overflowEllipsis_1.default);
var RightAlignColumn = styled_1.default(Column)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=groupTagValues.jsx.map