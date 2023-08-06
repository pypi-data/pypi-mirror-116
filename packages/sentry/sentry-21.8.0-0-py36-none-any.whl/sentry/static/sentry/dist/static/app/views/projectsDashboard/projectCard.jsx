Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectCard = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var round_1 = tslib_1.__importDefault(require("lodash/round"));
var projects_1 = require("app/actionCreators/projects");
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var bookmarkStar_1 = tslib_1.__importDefault(require("app/components/projects/bookmarkStar"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var scoreCard_1 = tslib_1.__importStar(require("app/components/scoreCard"));
var platformCategories_1 = require("app/data/platformCategories");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var projectsStatsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStatsStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var callIfFunction_1 = require("app/utils/callIfFunction");
var formatters_1 = require("app/utils/formatters");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var missingReleasesButtons_1 = tslib_1.__importStar(require("app/views/projectDetail/missingFeatureButtons/missingReleasesButtons"));
var utils_2 = require("app/views/releases/utils");
var chart_1 = tslib_1.__importDefault(require("./chart"));
var deploys_1 = tslib_1.__importStar(require("./deploys"));
var ProjectCard = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectCard, _super);
    function ProjectCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectCard.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, api = _a.api;
        // fetch project stats
        projects_1.loadStatsForProject(api, project.id, {
            orgId: organization.slug,
            projectId: project.id,
            query: {
                transactionStats: this.hasPerformance ? '1' : undefined,
                sessionStats: '1',
            },
        });
    };
    Object.defineProperty(ProjectCard.prototype, "hasPerformance", {
        get: function () {
            return this.props.organization.features.includes('performance-view');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCard.prototype, "crashFreeTrend", {
        get: function () {
            var _a = this.props.project.sessionStats || {}, currentCrashFreeRate = _a.currentCrashFreeRate, previousCrashFreeRate = _a.previousCrashFreeRate;
            if (!utils_1.defined(currentCrashFreeRate) || !utils_1.defined(previousCrashFreeRate)) {
                return undefined;
            }
            return round_1.default(currentCrashFreeRate - previousCrashFreeRate, currentCrashFreeRate > utils_2.CRASH_FREE_DECIMAL_THRESHOLD ? 3 : 0);
        },
        enumerable: false,
        configurable: true
    });
    ProjectCard.prototype.renderMissingFeatureCard = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        if (project.platform && platformCategories_1.releaseHealth.includes(project.platform)) {
            return (<scoreCard_1.default title={locale_1.t('Crash Free Sessions')} score={<missingReleasesButtons_1.default organization={organization} health/>}/>);
        }
        return (<scoreCard_1.default title={locale_1.t('Crash Free Sessions')} score={<NotAvailable>
            {locale_1.t('Not Available')}
            <questionTooltip_1.default title={locale_1.t('Release Health is not yet supported on this platform.')} size="xs"/>
          </NotAvailable>}/>);
    };
    ProjectCard.prototype.renderTrend = function () {
        var currentCrashFreeRate = (this.props.project.sessionStats || {}).currentCrashFreeRate;
        if (!utils_1.defined(currentCrashFreeRate) || !utils_1.defined(this.crashFreeTrend)) {
            return null;
        }
        return (<div>
        {this.crashFreeTrend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        {formatters_1.formatAbbreviatedNumber(Math.abs(this.crashFreeTrend)) + "%"}
      </div>);
    };
    ProjectCard.prototype.render = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, project = _c.project, hasProjectAccess = _c.hasProjectAccess;
        var stats = project.stats, slug = project.slug, transactionStats = project.transactionStats, sessionStats = project.sessionStats;
        var _d = sessionStats || {}, hasHealthData = _d.hasHealthData, currentCrashFreeRate = _d.currentCrashFreeRate;
        var totalErrors = (_a = stats === null || stats === void 0 ? void 0 : stats.reduce(function (sum, _a) {
            var _b = tslib_1.__read(_a, 2), _ = _b[0], value = _b[1];
            return sum + value;
        }, 0)) !== null && _a !== void 0 ? _a : 0;
        var totalTransactions = (_b = transactionStats === null || transactionStats === void 0 ? void 0 : transactionStats.reduce(function (sum, _a) {
            var _b = tslib_1.__read(_a, 2), _ = _b[0], value = _b[1];
            return sum + value;
        }, 0)) !== null && _b !== void 0 ? _b : 0;
        var zeroTransactions = totalTransactions === 0;
        var hasFirstEvent = Boolean(project.firstEvent || project.firstTransactionEvent);
        return (<div data-test-id={slug}>
        <StyledProjectCard>
          <CardHeader>
            <HeaderRow>
              <StyledIdBadge project={project} avatarSize={18} hideOverflow disableLink={!hasProjectAccess}/>
              <bookmarkStar_1.default organization={organization} project={project}/>
            </HeaderRow>
            <SummaryLinks>
              {stats ? (<react_1.Fragment>
                  <link_1.default data-test-id="project-errors" to={"/organizations/" + organization.slug + "/issues/?project=" + project.id}>
                    {locale_1.t('errors: %s', formatters_1.formatAbbreviatedNumber(totalErrors))}
                  </link_1.default>
                  {this.hasPerformance && (<react_1.Fragment>
                      <em>|</em>
                      <TransactionsLink data-test-id="project-transactions" to={"/organizations/" + organization.slug + "/performance/?project=" + project.id}>
                        {locale_1.t('transactions: %s', formatters_1.formatAbbreviatedNumber(totalTransactions))}
                        {zeroTransactions && (<questionTooltip_1.default title={locale_1.t('Click here to learn more about performance monitoring')} position="top" size="xs"/>)}
                      </TransactionsLink>
                    </react_1.Fragment>)}
                </react_1.Fragment>) : (<SummaryLinkPlaceholder />)}
            </SummaryLinks>
          </CardHeader>
          <ChartContainer>
            {stats ? (<chart_1.default firstEvent={hasFirstEvent} stats={stats} transactionStats={transactionStats}/>) : (<placeholder_1.default height="150px"/>)}
          </ChartContainer>
          <FooterWrapper>
            <ScoreCardWrapper>
              {!stats ? (<react_1.Fragment>
                  <ReleaseTitle>{locale_1.t('Crash Free Sessions')}</ReleaseTitle>
                  <FooterPlaceholder />
                </react_1.Fragment>) : hasHealthData ? (<scoreCard_1.default title={locale_1.t('Crash Free Sessions')} score={utils_1.defined(currentCrashFreeRate)
                    ? utils_2.displayCrashFreePercent(currentCrashFreeRate)
                    : '\u2014'} trend={this.renderTrend()} trendStatus={this.crashFreeTrend
                    ? this.crashFreeTrend > 0
                        ? 'good'
                        : 'bad'
                    : undefined}/>) : (this.renderMissingFeatureCard())}
            </ScoreCardWrapper>
            <DeploysWrapper>
              <ReleaseTitle>{locale_1.t('Latest Deploys')}</ReleaseTitle>
              {stats ? <deploys_1.default project={project} shorten/> : <FooterPlaceholder />}
            </DeploysWrapper>
          </FooterWrapper>
        </StyledProjectCard>
      </div>);
    };
    return ProjectCard;
}(react_1.Component));
exports.ProjectCard = ProjectCard;
var ProjectCardContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectCardContainer, _super);
    function ProjectCardContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.listeners = [
            projectsStatsStore_1.default.listen(function (itemsBySlug) {
                _this.onProjectStoreUpdate(itemsBySlug);
            }, undefined),
        ];
        return _this;
    }
    ProjectCardContainer.prototype.getInitialState = function () {
        var project = this.props.project;
        var initialState = projectsStatsStore_1.default.getInitialState() || {};
        return {
            projectDetails: initialState[project.slug] || null,
        };
    };
    ProjectCardContainer.prototype.componentWillUnmount = function () {
        this.listeners.forEach(callIfFunction_1.callIfFunction);
    };
    ProjectCardContainer.prototype.onProjectStoreUpdate = function (itemsBySlug) {
        var project = this.props.project;
        // Don't update state if we already have stats
        if (!itemsBySlug[project.slug]) {
            return;
        }
        if (itemsBySlug[project.slug] === this.state.projectDetails) {
            return;
        }
        this.setState({
            projectDetails: itemsBySlug[project.slug],
        });
    };
    ProjectCardContainer.prototype.render = function () {
        var _a = this.props, project = _a.project, props = tslib_1.__rest(_a, ["project"]);
        var projectDetails = this.state.projectDetails;
        return (<ProjectCard {...props} project={tslib_1.__assign(tslib_1.__assign({}, project), (projectDetails || {}))}/>);
    };
    return ProjectCardContainer;
}(react_1.Component));
var ChartContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  background: ", ";\n"], ["\n  position: relative;\n  background: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; });
var CardHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: ", " ", ";\n"], ["\n  margin: ", " ", ";\n"])), space_1.default(1.5), space_1.default(2));
var HeaderRow = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  justify-content: space-between;\n  align-items: center;\n"])));
var StyledProjectCard = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  min-height: 330px;\n"], ["\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  min-height: 330px;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowLight; });
var FooterWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  div {\n    border: none;\n    box-shadow: none;\n    font-size: ", ";\n    padding: 0;\n  }\n  ", " {\n    a {\n      background-color: ", ";\n      border: 1px solid ", ";\n      border-radius: ", ";\n      color: ", ";\n    }\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  div {\n    border: none;\n    box-shadow: none;\n    font-size: ", ";\n    padding: 0;\n  }\n  ", " {\n    a {\n      background-color: ", ";\n      border: 1px solid ", ";\n      border-radius: ", ";\n      color: ", ";\n    }\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, missingReleasesButtons_1.StyledButtonBar, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.gray500; });
var ScoreCardWrapper = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0 0 ", ";\n  ", " {\n    min-height: auto;\n  }\n  ", " {\n    color: ", ";\n    font-weight: 600;\n  }\n  ", " {\n    flex-direction: column;\n    align-items: flex-start;\n  }\n  ", " {\n    font-size: 28px;\n  }\n  ", " {\n    margin-left: 0;\n    margin-top: ", ";\n  }\n"], ["\n  margin: ", " 0 0 ", ";\n  ", " {\n    min-height: auto;\n  }\n  ", " {\n    color: ", ";\n    font-weight: 600;\n  }\n  ", " {\n    flex-direction: column;\n    align-items: flex-start;\n  }\n  ", " {\n    font-size: 28px;\n  }\n  ", " {\n    margin-left: 0;\n    margin-top: ", ";\n  }\n"])), space_1.default(2), space_1.default(2), scoreCard_1.StyledPanel, scoreCard_1.HeaderTitle, function (p) { return p.theme.gray300; }, scoreCard_1.ScoreWrapper, scoreCard_1.Score, scoreCard_1.Trend, space_1.default(0.5));
var DeploysWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  ", " {\n    display: block;\n    height: 100%;\n  }\n  ", " {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    grid-column-gap: ", ";\n    div {\n      white-space: nowrap;\n      text-overflow: ellipsis;\n      overflow: hidden;\n    }\n    a {\n      display: grid;\n    }\n  }\n  ", " {\n    grid-template-columns: 2fr auto;\n    margin-right: ", ";\n    height: auto;\n    svg {\n      display: none;\n    }\n  }\n"], ["\n  margin-top: ", ";\n  ", " {\n    display: block;\n    height: 100%;\n  }\n  ", " {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    grid-column-gap: ", ";\n    div {\n      white-space: nowrap;\n      text-overflow: ellipsis;\n      overflow: hidden;\n    }\n    a {\n      display: grid;\n    }\n  }\n  ", " {\n    grid-template-columns: 2fr auto;\n    margin-right: ", ";\n    height: auto;\n    svg {\n      display: none;\n    }\n  }\n"])), space_1.default(2), deploys_1.GetStarted, deploys_1.TextOverflow, space_1.default(1), deploys_1.DeployRows, space_1.default(2));
var ReleaseTitle = styled_1.default('span')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: 600;\n"], ["\n  color: ", ";\n  font-weight: 600;\n"])), function (p) { return p.theme.gray300; });
var StyledIdBadge = styled_1.default(idBadge_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"])));
var SummaryLinks = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  color: ", ";\n  font-size: ", ";\n\n  /* Need to offset for the project icon and margin */\n  margin-left: 26px;\n\n  a {\n    color: ", ";\n    :hover {\n      color: ", ";\n    }\n  }\n  em {\n    font-style: normal;\n    margin: 0 ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  color: ", ";\n  font-size: ", ";\n\n  /* Need to offset for the project icon and margin */\n  margin-left: 26px;\n\n  a {\n    color: ", ";\n    :hover {\n      color: ", ";\n    }\n  }\n  em {\n    font-style: normal;\n    margin: 0 ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.formText; }, function (p) { return p.theme.subText; }, space_1.default(0.5));
var TransactionsLink = styled_1.default(link_1.default)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  > span {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  > span {\n    margin-left: ", ";\n  }\n"])), space_1.default(0.5));
var NotAvailable = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5));
var SummaryLinkPlaceholder = styled_1.default(placeholder_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  height: 15px;\n  width: 180px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  height: 15px;\n  width: 180px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
var FooterPlaceholder = styled_1.default(placeholder_1.default)(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  height: 40px;\n  width: auto;\n  margin-right: ", ";\n"], ["\n  height: 40px;\n  width: auto;\n  margin-right: ", ";\n"])), space_1.default(2));
exports.default = withOrganization_1.default(withApi_1.default(ProjectCardContainer));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=projectCard.jsx.map