Object.defineProperty(exports, "__esModule", { value: true });
exports.PERFORMANCE_TOUR_STEPS = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var performance_empty_state_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-empty-state.svg"));
var performance_tour_alert_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-alert.svg"));
var performance_tour_correlate_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-correlate.svg"));
var performance_tour_metrics_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-metrics.svg"));
var performance_tour_trace_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/performance-tour-trace.svg"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureTourModal_1 = tslib_1.__importStar(require("app/components/modals/featureTourModal"));
var onboardingPanel_1 = tslib_1.__importDefault(require("app/components/onboardingPanel"));
var locale_1 = require("app/locale");
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var performanceSetupUrl = 'https://docs.sentry.io/performance-monitoring/getting-started/';
var docsLink = (<button_1.default external href={performanceSetupUrl}>
    {locale_1.t('Setup')}
  </button_1.default>);
exports.PERFORMANCE_TOUR_STEPS = [
    {
        title: locale_1.t('Track Application Metrics'),
        image: <featureTourModal_1.TourImage src={performance_tour_metrics_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Monitor your slowest pageloads and APIs to see which users are having the worst time.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Correlate Errors and Performance'),
        image: <featureTourModal_1.TourImage src={performance_tour_correlate_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('See what errors occurred within a transaction and the impact of those errors.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Watch and Alert'),
        image: <featureTourModal_1.TourImage src={performance_tour_alert_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t('Highlight mission-critical pages and APIs and set latency alerts to notify you before things go wrong.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: locale_1.t('Trace Across Systems'),
        image: <featureTourModal_1.TourImage src={performance_tour_trace_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {locale_1.t("Follow a trace from a user's session and drill down to identify any bottlenecks that occur.")}
      </featureTourModal_1.TourText>),
    },
];
function Onboarding(_a) {
    var _this = this;
    var organization = _a.organization, project = _a.project, api = _a.api;
    function handleAdvance(step, duration) {
        advancedAnalytics_1.trackAdvancedAnalyticsEvent('performance_views.tour.advance', {
            step: step,
            duration: duration,
            organization: organization,
        });
    }
    function handleClose(step, duration) {
        advancedAnalytics_1.trackAdvancedAnalyticsEvent('performance_views.tour.close', {
            step: step,
            duration: duration,
            organization: organization,
        });
    }
    var showSampleTransactionBtn = organization.features.includes('performance-create-sample-transaction');
    var featureTourBtn = (<featureTourModal_1.default steps={exports.PERFORMANCE_TOUR_STEPS} onAdvance={handleAdvance} onCloseModal={handleClose} doneUrl={performanceSetupUrl} doneText={locale_1.t('Start Setup')}>
      {function (_a) {
            var showModal = _a.showModal;
            return (<button_1.default priority={showSampleTransactionBtn ? 'link' : 'default'} onClick={function () {
                    advancedAnalytics_1.trackAdvancedAnalyticsEvent('performance_views.tour.start', { organization: organization });
                    showModal();
                }}>
          {locale_1.t('Take a Tour')}
        </button_1.default>);
        }}
    </featureTourModal_1.default>);
    var secondaryBtn = showSampleTransactionBtn ? (<button_1.default data-test-id="create-sample-transaction-btn" onClick={function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var url, eventData, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        advancedAnalytics_1.trackAdvancedAnalyticsEvent('performance_views.create_sample_transaction', {
                            platform: project.platform,
                            organization: organization,
                        });
                        indicator_1.addLoadingMessage(locale_1.t('Processing sample event...'), {
                            duration: 15000,
                        });
                        url = "/projects/" + organization.slug + "/" + project.slug + "/create-sample-transaction/";
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(url, { method: 'POST' })];
                    case 2:
                        eventData = _a.sent();
                        react_router_1.browserHistory.push("/organizations/" + organization.slug + "/performance/" + project.slug + ":" + eventData.eventID + "/");
                        indicator_1.clearIndicators();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        Sentry.withScope(function (scope) {
                            scope.setExtra('error', error_1);
                            Sentry.captureException(new Error('Failed to create sample event'));
                        });
                        indicator_1.clearIndicators();
                        indicator_1.addErrorMessage(locale_1.t('Failed to create a new sample event'));
                        return [2 /*return*/];
                    case 4: return [2 /*return*/];
                }
            });
        }); }}>
      {locale_1.t('Create Sample Transaction')}
    </button_1.default>) : (featureTourBtn);
    return (<onboardingPanel_1.default image={<PerfImage src={performance_empty_state_svg_1.default}/>}>
      <h3>{locale_1.t('Pinpoint problems')}</h3>
      <p>
        {locale_1.t('Something seem slow? Track down transactions to connect the dots between 10-second page loads and poor-performing API calls or slow database queries.')}
      </p>
      <ButtonList gap={1}>
        <button_1.default priority="primary" target="_blank" href="https://docs.sentry.io/performance-monitoring/getting-started/">
          {locale_1.t('Start Setup')}
        </button_1.default>
        {secondaryBtn}
      </ButtonList>
      {showSampleTransactionBtn && featureTourBtn}
    </onboardingPanel_1.default>);
}
var PerfImage = styled_1.default('img')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 75px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 75px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var ButtonList = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n  margin-bottom: 16px;\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n  margin-bottom: 16px;\n"])));
exports.default = withApi_1.default(Onboarding);
var templateObject_1, templateObject_2;
//# sourceMappingURL=onboarding.jsx.map