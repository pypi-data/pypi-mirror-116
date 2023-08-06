Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var utils_1 = require("app/views/releases/utils");
describe('releases/details/utils', function () {
    describe('getReleaseBounds', function () {
        it('returns start and end of a release', function () {
            // @ts-expect-error
            expect(utils_1.getReleaseBounds(TestStubs.Release())).toEqual({
                releaseStart: '2020-03-23T01:02:00Z',
                releaseEnd: '2020-03-24T02:04:00Z',
            });
        });
        it('higher last session takes precendence over last event', function () {
            expect(utils_1.getReleaseBounds(
            // @ts-expect-error
            TestStubs.Release({
                currentProjectMeta: { sessionsUpperBound: '2020-03-24T03:04:55Z' },
            }))).toEqual({
                releaseStart: '2020-03-23T01:02:00Z',
                releaseEnd: '2020-03-24T03:04:00Z',
            });
        });
        it('there is no last session/event, it fallbacks to now', function () {
            // @ts-expect-error
            expect(utils_1.getReleaseBounds(TestStubs.Release({ lastEvent: null }))).toEqual({
                releaseStart: '2020-03-23T01:02:00Z',
                releaseEnd: '2017-10-17T02:41:00Z',
            });
        });
        it('adds 1 minute to end if start and end are within same minute', function () {
            expect(utils_1.getReleaseBounds(
            // @ts-expect-error
            TestStubs.Release({
                dateCreated: '2020-03-23T01:02:30Z',
                lastEvent: '2020-03-23T01:02:39Z',
            }))).toEqual({
                releaseStart: '2020-03-23T01:02:00Z',
                releaseEnd: '2020-03-23T01:03:00Z',
            });
        });
    });
    describe('getReleaseParams', function () {
        var routerContext = initializeOrg_1.initializeOrg().routerContext;
        // @ts-expect-error
        var releaseBounds = utils_1.getReleaseBounds(TestStubs.Release());
        var defaultStatsPeriod = '14d';
        var allowEmptyPeriod = true;
        it('returns params related to a release', function () {
            var location = tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: {
                    pageStatsPeriod: '30d',
                    project: ['456'],
                    environment: ['prod'],
                    somethingBad: 'meh',
                } });
            expect(utils_1.getReleaseParams({
                location: location,
                releaseBounds: releaseBounds,
                defaultStatsPeriod: defaultStatsPeriod,
                allowEmptyPeriod: allowEmptyPeriod,
            })).toEqual({
                statsPeriod: '30d',
                project: ['456'],
                environment: ['prod'],
            });
        });
        it('returns release start/end if no other datetime is present', function () {
            expect(utils_1.getReleaseParams({
                location: tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: {} }),
                releaseBounds: releaseBounds,
                defaultStatsPeriod: defaultStatsPeriod,
                allowEmptyPeriod: allowEmptyPeriod,
            })).toEqual({
                start: '2020-03-23T01:02:00Z',
                end: '2020-03-24T02:04:00Z',
            });
        });
        it('returns correct start/end when zoomed in', function () {
            expect(utils_1.getReleaseParams({
                location: tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: { pageStart: '2021-03-23T01:02:30Z', pageEnd: '2022-03-23T01:02:30Z' } }),
                releaseBounds: releaseBounds,
                defaultStatsPeriod: defaultStatsPeriod,
                allowEmptyPeriod: allowEmptyPeriod,
            })).toEqual({
                start: '2021-03-23T01:02:30.000',
                end: '2022-03-23T01:02:30.000',
            });
        });
        // used in releases without release-comparison feature flag
        it('returns default stats period', function () {
            expect(utils_1.getReleaseParams({
                location: tslib_1.__assign(tslib_1.__assign({}, routerContext.location), { query: {} }),
                releaseBounds: releaseBounds,
                defaultStatsPeriod: '7d',
                allowEmptyPeriod: false,
            })).toEqual({
                statsPeriod: '7d',
            });
        });
    });
});
//# sourceMappingURL=index.spec.jsx.map