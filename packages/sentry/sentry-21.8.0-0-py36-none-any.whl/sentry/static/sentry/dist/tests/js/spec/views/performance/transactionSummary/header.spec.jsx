Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var header_1 = tslib_1.__importStar(require("app/views/performance/transactionSummary/header"));
function initializeData(opts) {
    // @ts-expect-error
    var project = TestStubs.Project({ platform: opts === null || opts === void 0 ? void 0 : opts.platform });
    // @ts-expect-error
    var organization = TestStubs.Organization({
        projects: [project],
    });
    var initialData = initializeOrg_1.initializeOrg({
        organization: organization,
        router: {
            location: {
                query: {
                    project: project.id,
                },
            },
        },
        project: project.id,
        projects: [],
    });
    var router = initialData.router;
    var eventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        version: 2,
        name: '',
        fields: ['transaction.status'],
        projects: [parseInt(project.id, 10)],
    });
    return {
        project: project,
        organization: organization,
        router: router,
        eventView: eventView,
    };
}
describe('Performance > Transaction Summary Header', function () {
    var wrapper;
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
        wrapper.unmount();
    });
    it('should render web vitals tab when yes', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, project, organization, router, eventView;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = initializeData(), project = _a.project, organization = _a.organization, router = _a.router, eventView = _a.eventView;
                        wrapper = enzyme_1.mountWithTheme(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} transactionName="transaction_name" currentTab={header_1.Tab.TransactionSummary} hasWebVitals="yes" handleIncompatibleQuery={function () { }}/>);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeTruthy();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('should not render web vitals tab when no', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, project, organization, router, eventView;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = initializeData(), project = _a.project, organization = _a.organization, router = _a.router, eventView = _a.eventView;
                        wrapper = enzyme_1.mountWithTheme(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} transactionName="transaction_name" currentTab={header_1.Tab.TransactionSummary} hasWebVitals="no" handleIncompatibleQuery={function () { }}/>);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeFalsy();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('should render web vitals tab when maybe and is frontend platform', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, project, organization, router, eventView;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = initializeData({
                            platform: 'javascript',
                        }), project = _a.project, organization = _a.organization, router = _a.router, eventView = _a.eventView;
                        wrapper = enzyme_1.mountWithTheme(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} transactionName="transaction_name" currentTab={header_1.Tab.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={function () { }}/>);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeTruthy();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('should render web vitals tab when maybe and has measurements', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, project, organization, router, eventView;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: '/organizations/org-slug/events-has-measurements/',
                            body: { measurements: true },
                        });
                        _a = initializeData(), project = _a.project, organization = _a.organization, router = _a.router, eventView = _a.eventView;
                        wrapper = enzyme_1.mountWithTheme(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} transactionName="transaction_name" currentTab={header_1.Tab.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={function () { }}/>);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeTruthy();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('should not render web vitals tab when maybe and has no measurements', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, project, organization, router, eventView;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: '/organizations/org-slug/events-has-measurements/',
                            body: { measurements: false },
                        });
                        _a = initializeData(), project = _a.project, organization = _a.organization, router = _a.router, eventView = _a.eventView;
                        wrapper = enzyme_1.mountWithTheme(<header_1.default eventView={eventView} location={router.location} organization={organization} projects={[project]} transactionName="transaction_name" currentTab={header_1.Tab.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={function () { }}/>);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('ListLink[data-test-id="web-vitals-tab"]').exists()).toBeFalsy();
                        return [2 /*return*/];
                }
            });
        });
    });
});
//# sourceMappingURL=header.spec.jsx.map