Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var paginationCaption_1 = tslib_1.__importDefault(require("app/components/pagination/paginationCaption"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var rangeSlider_1 = tslib_1.__importStar(require("app/views/settings/components/forms/controls/rangeSlider"));
var errorMessage_1 = tslib_1.__importDefault(require("./errorMessage"));
var newIssue_1 = tslib_1.__importDefault(require("./newIssue"));
function LinkFooter() {
    return (<Footer>
      <externalLink_1.default href={"mailto:grouping@sentry.io?subject=" + encodeURIComponent('Grouping Feedback') + "&body=" + encodeURIComponent("URL: " + window.location.href + "\n\nThanks for taking the time to provide us feedback. What's on your mind?")}>
        <StyledIconMegaphone /> {locale_1.t('Give Feedback')}
      </externalLink_1.default>
    </Footer>);
}
function Grouping(_a) {
    var _b, _c;
    var api = _a.api, groupId = _a.groupId, location = _a.location, organization = _a.organization, router = _a.router, projSlug = _a.projSlug;
    var _d = location.query, cursor = _d.cursor, level = _d.level;
    var _e = tslib_1.__read(react_1.useState(false), 2), isLoading = _e[0], setIsLoading = _e[1];
    var _f = tslib_1.__read(react_1.useState(false), 2), isGroupingLevelDetailsLoading = _f[0], setIsGroupingLevelDetailsLoading = _f[1];
    var _g = tslib_1.__read(react_1.useState(undefined), 2), error = _g[0], setError = _g[1];
    var _h = tslib_1.__read(react_1.useState([]), 2), groupingLevels = _h[0], setGroupingLevels = _h[1];
    var _j = tslib_1.__read(react_1.useState(undefined), 2), activeGroupingLevel = _j[0], setActiveGroupingLevel = _j[1];
    var _k = tslib_1.__read(react_1.useState([]), 2), activeGroupingLevelDetails = _k[0], setActiveGroupingLevelDetails = _k[1];
    var _l = tslib_1.__read(react_1.useState(''), 2), pagination = _l[0], setPagination = _l[1];
    react_1.useEffect(function () {
        fetchGroupingLevels();
    }, []);
    react_1.useEffect(function () {
        setSecondGrouping();
    }, [groupingLevels]);
    react_1.useEffect(function () {
        updateUrlWithNewLevel();
    }, [activeGroupingLevel]);
    react_1.useEffect(function () {
        fetchGroupingLevelDetails();
    }, [activeGroupingLevel, cursor]);
    var handleSetActiveGroupingLevel = debounce_1.default(function (groupingLevelId) {
        setActiveGroupingLevel(Number(groupingLevelId));
    }, constants_1.DEFAULT_DEBOUNCE_DURATION);
    function fetchGroupingLevels() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        setError(undefined);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/grouping/levels/")];
                    case 2:
                        response = _a.sent();
                        setIsLoading(false);
                        setGroupingLevels(response.levels);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        setIsLoading(false);
                        setError(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function fetchGroupingLevelDetails() {
        var _a;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _b, data, resp, pageLinks, err_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (!groupingLevels.length || !utils_1.defined(activeGroupingLevel)) {
                            return [2 /*return*/];
                        }
                        setIsGroupingLevelDetailsLoading(true);
                        setError(undefined);
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/grouping/levels/" + activeGroupingLevel + "/new-issues/", {
                                method: 'GET',
                                includeAllArgs: true,
                                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { per_page: 10 }),
                            })];
                    case 2:
                        _b = tslib_1.__read.apply(void 0, [_c.sent(), 3]), data = _b[0], resp = _b[2];
                        pageLinks = (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader) === null || _a === void 0 ? void 0 : _a.call(resp, 'Link');
                        setPagination(pageLinks !== null && pageLinks !== void 0 ? pageLinks : '');
                        setActiveGroupingLevelDetails(Array.isArray(data) ? data : [data]);
                        setIsGroupingLevelDetailsLoading(false);
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        setIsGroupingLevelDetailsLoading(false);
                        setError(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function updateUrlWithNewLevel() {
        if (!utils_1.defined(activeGroupingLevel) || level === activeGroupingLevel) {
            return;
        }
        router.replace({
            pathname: location.pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, level: activeGroupingLevel }),
        });
    }
    function setSecondGrouping() {
        if (!groupingLevels.length) {
            return;
        }
        if (utils_1.defined(level)) {
            if (!utils_1.defined(groupingLevels[level])) {
                setError(locale_1.t('The level you were looking for was not found.'));
                return;
            }
            if (level === activeGroupingLevel) {
                return;
            }
            setActiveGroupingLevel(level);
            return;
        }
        if (groupingLevels.length > 1) {
            setActiveGroupingLevel(groupingLevels[1].id);
            return;
        }
        setActiveGroupingLevel(groupingLevels[0].id);
    }
    if (isLoading) {
        return <loadingIndicator_1.default />;
    }
    if (error) {
        return (<react_1.default.Fragment>
        <errorMessage_1.default onRetry={fetchGroupingLevels} groupId={groupId} error={error} projSlug={projSlug} orgSlug={organization.slug}/>
        <LinkFooter />
      </react_1.default.Fragment>);
    }
    if (!activeGroupingLevelDetails.length) {
        return <loadingIndicator_1.default />;
    }
    var links = parseLinkHeader_1.default(pagination);
    var hasMore = ((_b = links.previous) === null || _b === void 0 ? void 0 : _b.results) || ((_c = links.next) === null || _c === void 0 ? void 0 : _c.results);
    var paginationCurrentQuantity = activeGroupingLevelDetails.length;
    return (<Wrapper>
      <Header>
        {locale_1.t('This issue is an aggregate of multiple events that sentry determined originate from the same root-cause. Use this page to explore more detailed groupings that exist within this issue.')}
      </Header>
      <Body>
        <SliderWrapper>
          {locale_1.t('Fewer issues')}
          <StyledRangeSlider name="grouping-level" allowedValues={groupingLevels.map(function (groupingLevel) { return Number(groupingLevel.id); })} value={activeGroupingLevel !== null && activeGroupingLevel !== void 0 ? activeGroupingLevel : 0} onChange={handleSetActiveGroupingLevel} showLabel={false}/>
          {locale_1.t('More issues')}
        </SliderWrapper>
        <Content isReloading={isGroupingLevelDetailsLoading}>
          <StyledPanelTable headers={['', locale_1.t('Events')]}>
            {activeGroupingLevelDetails.map(function (_a) {
            var hash = _a.hash, title = _a.title, metadata = _a.metadata, latestEvent = _a.latestEvent, eventCount = _a.eventCount;
            // XXX(markus): Ugly hack to make NewIssue show the right things.
            return (<newIssue_1.default key={hash} sampleEvent={tslib_1.__assign(tslib_1.__assign({}, latestEvent), { metadata: metadata || latestEvent.metadata, title: title || latestEvent.title })} eventCount={eventCount} organization={organization}/>);
        })}
          </StyledPanelTable>
          <StyledPagination pageLinks={pagination} disabled={isGroupingLevelDetailsLoading} caption={<paginationCaption_1.default caption={locale_1.tct('Showing [current] of [total] [result]', {
                result: hasMore
                    ? locale_1.t('results')
                    : locale_1.tn('result', 'results', paginationCurrentQuantity),
                current: paginationCurrentQuantity,
                total: hasMore
                    ? paginationCurrentQuantity + "+"
                    : paginationCurrentQuantity,
            })}/>}/>
        </Content>
      </Body>
      <LinkFooter />
    </Wrapper>);
}
exports.default = withApi_1.default(Grouping);
var StyledIconMegaphone = styled_1.default(icons_1.IconMegaphone)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  display: grid;\n  align-content: flex-start;\n  margin: -", " -", ";\n  padding: ", " ", ";\n"], ["\n  flex: 1;\n  display: grid;\n  align-content: flex-start;\n  margin: -", " -", ";\n  padding: ", " ", ";\n"])), space_1.default(3), space_1.default(4), space_1.default(3), space_1.default(4));
var Header = styled_1.default('p')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  && {\n    margin-bottom: ", ";\n  }\n"], ["\n  && {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(2));
var Footer = styled_1.default('p')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  && {\n    margin-top: ", ";\n  }\n"], ["\n  && {\n    margin-top: ", ";\n  }\n"])), space_1.default(2));
var Body = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(3));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: 1fr minmax(60px, auto);\n  > * {\n    padding: ", " ", ";\n    :nth-child(-n + 2) {\n      padding: ", ";\n    }\n    :nth-child(2n) {\n      display: flex;\n      text-align: right;\n      justify-content: flex-end;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr minmax(80px, auto);\n  }\n"], ["\n  grid-template-columns: 1fr minmax(60px, auto);\n  > * {\n    padding: ", " ", ";\n    :nth-child(-n + 2) {\n      padding: ", ";\n    }\n    :nth-child(2n) {\n      display: flex;\n      text-align: right;\n      justify-content: flex-end;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr minmax(80px, auto);\n  }\n"])), space_1.default(1.5), space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[3]; });
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var Content = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.isReloading &&
        "\n      " + StyledPanelTable + ", " + StyledPagination + " {\n        opacity: 0.5;\n        pointer-events: none;\n      }\n    ";
});
var SliderWrapper = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content max-content;\n  justify-content: space-between;\n  align-items: flex-start;\n  position: relative;\n  font-size: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n\n  @media (min-width: 700px) {\n    grid-template-columns: max-content minmax(270px, auto) max-content;\n    align-items: center;\n    justify-content: flex-start;\n    padding-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content max-content;\n  justify-content: space-between;\n  align-items: flex-start;\n  position: relative;\n  font-size: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n\n  @media (min-width: 700px) {\n    grid-template-columns: max-content minmax(270px, auto) max-content;\n    align-items: center;\n    justify-content: flex-start;\n    padding-bottom: 0;\n  }\n"])), space_1.default(1.5), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space_1.default(2));
var StyledRangeSlider = styled_1.default(rangeSlider_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  ", " {\n    background: transparent;\n    margin-top: 0;\n    margin-bottom: 0;\n\n    ::-ms-thumb {\n      box-shadow: 0 0 0 3px ", ";\n    }\n\n    ::-moz-range-thumb {\n      box-shadow: 0 0 0 3px ", ";\n    }\n\n    ::-webkit-slider-thumb {\n      box-shadow: 0 0 0 3px ", ";\n    }\n  }\n\n  position: absolute;\n  bottom: 0;\n  left: ", ";\n  right: ", ";\n\n  @media (min-width: 700px) {\n    position: static;\n    left: auto;\n    right: auto;\n  }\n"], ["\n  ", " {\n    background: transparent;\n    margin-top: 0;\n    margin-bottom: 0;\n\n    ::-ms-thumb {\n      box-shadow: 0 0 0 3px ", ";\n    }\n\n    ::-moz-range-thumb {\n      box-shadow: 0 0 0 3px ", ";\n    }\n\n    ::-webkit-slider-thumb {\n      box-shadow: 0 0 0 3px ", ";\n    }\n  }\n\n  position: absolute;\n  bottom: 0;\n  left: ", ";\n  right: ", ";\n\n  @media (min-width: 700px) {\n    position: static;\n    left: auto;\n    right: auto;\n  }\n"])), rangeSlider_1.Slider, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.backgroundSecondary; }, space_1.default(1.5), space_1.default(1.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=grouping.jsx.map