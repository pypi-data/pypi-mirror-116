Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var collapsible_1 = tslib_1.__importDefault(require("app/components/collapsible"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var list_1 = require("app/views/releases/list");
var utils_2 = require("../../utils");
var crashFree_1 = tslib_1.__importDefault(require("../crashFree"));
var healthStatsChart_1 = tslib_1.__importDefault(require("../healthStatsChart"));
var healthStatsPeriod_1 = tslib_1.__importDefault(require("../healthStatsPeriod"));
var utils_3 = require("../utils");
var header_1 = tslib_1.__importDefault(require("./header"));
var projectLink_1 = tslib_1.__importDefault(require("./projectLink"));
var ADOPTION_STAGE_LABELS = {
    low_adoption: {
        name: locale_1.t('Low Adoption'),
        tooltipTitle: locale_1.t('Never exceeded 10% adoption in a 6 hour period'),
        type: 'warning',
    },
    adopted: {
        name: locale_1.t('Adopted'),
        tooltipTitle: locale_1.t('At least 10% adoption in the last 6 hours'),
        type: 'success',
    },
    replaced: {
        name: locale_1.t('Replaced'),
        tooltipTitle: locale_1.t('Was previously adopted'),
        type: 'default',
    },
};
var Content = function (_a) {
    var projects = _a.projects, showReleaseAdoptionStages = _a.showReleaseAdoptionStages, adoptionStages = _a.adoptionStages, releaseVersion = _a.releaseVersion, location = _a.location, organization = _a.organization, activeDisplay = _a.activeDisplay, showPlaceholders = _a.showPlaceholders, isTopRelease = _a.isTopRelease, getHealthData = _a.getHealthData;
    return (<react_1.Fragment>
    <header_1.default>
      <Layout showReleaseAdoptionStages={showReleaseAdoptionStages}>
        <Column>{locale_1.t('Project Name')}</Column>
        {showReleaseAdoptionStages && (<AdoptionStageColumn>{locale_1.t('Adoption Stage')}</AdoptionStageColumn>)}
        <AdoptionColumn>
          <span>{locale_1.t('Adoption')}</span>
          <healthStatsPeriod_1.default location={location}/>
        </AdoptionColumn>
        <CrashFreeRateColumn>{locale_1.t('Crash Free Rate')}</CrashFreeRateColumn>
        <CrashesColumn>{locale_1.t('Crashes')}</CrashesColumn>
        <NewIssuesColumn>{locale_1.t('New Issues')}</NewIssuesColumn>
      </Layout>
    </header_1.default>

    <ProjectRows>
      <collapsible_1.default expandButton={function (_a) {
            var onExpand = _a.onExpand, numberOfHiddenItems = _a.numberOfHiddenItems;
            return (<ExpandButtonWrapper>
            <button_1.default priority="primary" size="xsmall" onClick={onExpand}>
              {locale_1.tct('Show [numberOfHiddenItems] More', { numberOfHiddenItems: numberOfHiddenItems })}
            </button_1.default>
          </ExpandButtonWrapper>);
        }} collapseButton={function (_a) {
            var onCollapse = _a.onCollapse;
            return (<CollapseButtonWrapper>
            <button_1.default priority="primary" size="xsmall" onClick={onCollapse}>
              {locale_1.t('Collapse')}
            </button_1.default>
          </CollapseButtonWrapper>);
        }}>
        {projects.map(function (project, index) {
            var id = project.id, slug = project.slug, newGroups = project.newGroups;
            var crashCount = getHealthData.getCrashCount(releaseVersion, id, utils_3.DisplayOption.SESSIONS);
            var crashFreeRate = getHealthData.getCrashFreeRate(releaseVersion, id, activeDisplay);
            var get24hCountByProject = getHealthData.get24hCountByProject(id, activeDisplay);
            var timeSeries = getHealthData.getTimeSeries(releaseVersion, id, activeDisplay);
            var adoption = getHealthData.getAdoption(releaseVersion, id, activeDisplay);
            // we currently don't support sub-hour session intervals, we rather hide the count histogram than to show only two bars
            var hasCountHistogram = (timeSeries === null || timeSeries === void 0 ? void 0 : timeSeries[0].data.length) > 7 &&
                timeSeries[0].data.some(function (item) { return item.value > 0; });
            var adoptionStage = showReleaseAdoptionStages &&
                (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages[project.slug]) &&
                (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages[project.slug].stage);
            var isMobileProject = list_1.isProjectMobileForReleases(project.platform);
            var adoptionStageLabel = Boolean(get24hCountByProject && adoptionStage && isMobileProject) &&
                ADOPTION_STAGE_LABELS[adoptionStage];
            return (<ProjectRow key={releaseVersion + "-" + slug + "-health"}>
              <Layout showReleaseAdoptionStages={showReleaseAdoptionStages}>
                <Column>
                  <projectBadge_1.default project={project} avatarSize={16}/>
                </Column>

                {showReleaseAdoptionStages && (<AdoptionStageColumn>
                    {adoptionStageLabel ? (<link_1.default to={{
                            pathname: "/organizations/" + organization.slug + "/releases/",
                            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: "release.stage:" + adoptionStage }),
                        }}>
                        <tooltip_1.default title={adoptionStageLabel.tooltipTitle}>
                          <tag_1.default type={adoptionStageLabel.type}>
                            {adoptionStageLabel.name}
                          </tag_1.default>
                        </tooltip_1.default>
                      </link_1.default>) : (<notAvailable_1.default />)}
                  </AdoptionStageColumn>)}

                <AdoptionColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="100px"/>) : adoption && hasCountHistogram ? (<AdoptionWrapper>
                      <span>{Math.round(adoption)}%</span>
                      <healthStatsChart_1.default data={timeSeries} height={20} activeDisplay={activeDisplay}/>
                    </AdoptionWrapper>) : (<notAvailable_1.default />)}
                </AdoptionColumn>

                <CrashFreeRateColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : utils_1.defined(crashFreeRate) ? (<crashFree_1.default percent={crashFreeRate}/>) : (<notAvailable_1.default />)}
                </CrashFreeRateColumn>

                <CrashesColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="30px"/>) : utils_1.defined(crashCount) ? (<tooltip_1.default title={locale_1.t('Open in Issues')}>
                      <globalSelectionLink_1.default to={utils_2.getReleaseUnhandledIssuesUrl(organization.slug, project.id, releaseVersion)}>
                        <count_1.default value={crashCount}/>
                      </globalSelectionLink_1.default>
                    </tooltip_1.default>) : (<notAvailable_1.default />)}
                </CrashesColumn>

                <NewIssuesColumn>
                  <tooltip_1.default title={locale_1.t('Open in Issues')}>
                    <globalSelectionLink_1.default to={utils_2.getReleaseNewIssuesUrl(organization.slug, project.id, releaseVersion)}>
                      <count_1.default value={newGroups || 0}/>
                    </globalSelectionLink_1.default>
                  </tooltip_1.default>
                </NewIssuesColumn>

                <ViewColumn>
                  <guideAnchor_1.default disabled={!isTopRelease || index !== 0} target="view_release">
                    <projectLink_1.default orgSlug={organization.slug} project={project} releaseVersion={releaseVersion} location={location}/>
                  </guideAnchor_1.default>
                </ViewColumn>
              </Layout>
            </ProjectRow>);
        })}
      </collapsible_1.default>
    </ProjectRows>
  </react_1.Fragment>);
};
exports.default = Content;
var ProjectRows = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ExpandButtonWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  width: 100%;\n  bottom: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-image: linear-gradient(\n    180deg,\n    hsla(0, 0%, 100%, 0.15) 0,\n    ", "\n  );\n  background-repeat: repeat-x;\n  border-bottom: ", " solid ", ";\n  border-top: ", " solid transparent;\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"], ["\n  position: absolute;\n  width: 100%;\n  bottom: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-image: linear-gradient(\n    180deg,\n    hsla(0, 0%, 100%, 0.15) 0,\n    ", "\n  );\n  background-repeat: repeat-x;\n  border-bottom: ", " solid ", ";\n  border-top: ", " solid transparent;\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"])), function (p) { return p.theme.white; }, space_1.default(1), function (p) { return p.theme.white; }, space_1.default(1), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.borderRadius; });
var CollapseButtonWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 41px;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 41px;\n"])));
var ProjectRow = styled_1.default(panels_1.PanelItem)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  padding: ", " ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"])), space_1.default(1), space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.fontSizeMedium; });
var Layout = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1.4fr 0.6fr 0.7fr;\n\n  grid-column-gap: ", ";\n  align-items: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1.4fr 0.6fr 0.7fr;\n\n  grid-column-gap: ", ";\n  align-items: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; }, function (p) {
    return p.showReleaseAdoptionStages
        ? "\n      grid-template-columns: 1fr 0.7fr 1fr 1fr 0.7fr 0.7fr 0.5fr;\n    "
        : "\n      grid-template-columns: 1fr 1fr 1fr 0.7fr 0.7fr 0.5fr;\n    ";
});
var Column = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", ";\n  line-height: 20px;\n"], ["\n  ", ";\n  line-height: 20px;\n"])), overflowEllipsis_1.default);
var NewIssuesColumn = styled_1.default(Column)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    text-align: right;\n  }\n"], ["\n  @media (min-width: ", ") {\n    text-align: right;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AdoptionColumn = styled_1.default(Column)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n\n  & > * {\n    flex: 1;\n  }\n"], ["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n\n  & > * {\n    flex: 1;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AdoptionStageColumn = styled_1.default(Column)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n\n    /* Need to show the edges of the tags */\n    overflow: visible;\n  }\n"], ["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n\n    /* Need to show the edges of the tags */\n    overflow: visible;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var AdoptionWrapper = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  display: inline-grid;\n  grid-template-columns: 30px 1fr;\n  grid-gap: ", ";\n  align-items: center;\n\n  /* Chart tooltips need overflow */\n  overflow: visible;\n"], ["\n  flex: 1;\n  display: inline-grid;\n  grid-template-columns: 30px 1fr;\n  grid-gap: ", ";\n  align-items: center;\n\n  /* Chart tooltips need overflow */\n  overflow: visible;\n"])), space_1.default(1));
var CrashFreeRateColumn = styled_1.default(Column)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    text-align: center;\n  }\n\n  @media (min-width: ", ") {\n    text-align: right;\n  }\n"], ["\n  @media (min-width: ", ") {\n    text-align: center;\n  }\n\n  @media (min-width: ", ") {\n    text-align: right;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[3]; });
var CrashesColumn = styled_1.default(Column)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    text-align: right;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    text-align: right;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ViewColumn = styled_1.default(Column)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var StyledPlaceholder = styled_1.default(placeholder_1.default)(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  height: 15px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"], ["\n  height: 15px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"])), space_1.default(0.25));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=content.jsx.map