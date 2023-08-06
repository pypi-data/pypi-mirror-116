Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
var releaseComparisonChart_1 = tslib_1.__importDefault(require("app/views/releases/detail/overview/releaseComparisonChart"));
describe('Releases > Detail > Overview > ReleaseComparison', function () {
    afterEach(function () {
        reactTestingLibrary_1.cleanup();
    });
    var _a = initializeOrg_1.initializeOrg(), routerContext = _a.routerContext, organization = _a.organization, project = _a.project;
    // @ts-expect-error
    var api = new MockApiClient();
    // @ts-expect-error
    var release = TestStubs.Release();
    // @ts-expect-error
    var releaseSessions = TestStubs.SessionUserCountByStatus();
    // @ts-expect-error
    var allSessions = TestStubs.SessionUserCountByStatus2();
    it('displays correct all/release/change data', function () {
        reactTestingLibrary_1.mountWithTheme(<releaseComparisonChart_1.default release={release} releaseSessions={releaseSessions} allSessions={allSessions} platform="javascript" location={tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: {} })} loading={false} reloading={false} errored={false} project={project} organization={organization} api={api} hasHealthData/>, { context: routerContext });
        expect(reactTestingLibrary_1.screen.getByLabelText('Chart Title').textContent).toBe('Crash Free Session Rate');
        expect(reactTestingLibrary_1.screen.getByLabelText('Chart Value').textContent).toContain('95.006% 4.51%');
        expect(reactTestingLibrary_1.screen.getAllByRole('radio').length).toBe(12);
        // lazy way to make sure that all percentages are calculated correctly
        expect(reactTestingLibrary_1.screen.getByTestId('release-comparison-table').textContent).toMatchInlineSnapshot(
        // eslint-disable-next-line no-irregular-whitespace
        "\"DescriptionAll ReleasesThis ReleaseChangeCrash Free Session Rate\u00A099.516%95.006%4.51% Healthy\u00A098.564%94.001%4.563% Abnormal\u00A00%0%0% \u2014Errored\u00A00.953%1.005%0.052% Crashed Session Rate\u00A00.484%4.994%4.511% Crash Free User Rate\u00A099.908%75%24.908% Healthy\u00A098.994%72.022%26.972% Abnormal\u00A00%0%0% \u2014Errored\u00A00.914%2.493%1.579% Crashed User Rate\u00A00.092%25.485%25.393% Session Count\u00A0205k9.8k\u2014User Count\u00A0100k361\u2014\"");
    });
    it('can change chart by clicking on a row', function () {
        var rerender = reactTestingLibrary_1.mountWithTheme(<releaseComparisonChart_1.default release={release} releaseSessions={releaseSessions} allSessions={allSessions} platform="javascript" location={tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: {} })} loading={false} reloading={false} errored={false} project={project} organization={organization} api={api} hasHealthData/>, { context: routerContext }).rerender;
        reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByLabelText(/crashed session rate/i));
        expect(react_router_1.browserHistory.push).toHaveBeenCalledWith({ query: { chart: 'crashedSessions' } });
        rerender(<releaseComparisonChart_1.default release={release} releaseSessions={releaseSessions} allSessions={allSessions} platform="javascript" location={tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: { chart: 'crashedSessions' } })} loading={false} reloading={false} errored={false} project={project} organization={organization} api={api} hasHealthData/>);
        expect(reactTestingLibrary_1.screen.getByLabelText('Chart Title').textContent).toBe('Crashed Session Rate');
        expect(reactTestingLibrary_1.screen.getByLabelText('Chart Value').textContent).toContain('4.994% 4.511%');
    });
});
//# sourceMappingURL=index.spec.jsx.map