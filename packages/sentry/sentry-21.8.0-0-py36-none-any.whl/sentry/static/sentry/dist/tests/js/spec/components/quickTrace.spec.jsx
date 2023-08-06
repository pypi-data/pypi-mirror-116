Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var quickTrace_1 = tslib_1.__importDefault(require("app/components/quickTrace"));
describe('Quick Trace', function () {
    var location;
    var organization;
    var initialize = function () {
        var context = initializeOrg_1.initializeOrg();
        organization = context.organization;
    };
    function makeQuickTraceEvents(generation, _a) {
        var _b = _a === void 0 ? {} : _a, _c = _b.n, n = _c === void 0 ? 1 : _c, _d = _b.parentId, parentId = _d === void 0 ? null : _d;
        var events = [];
        for (var i = 0; i < n; i++) {
            var suffix = n > 1 ? "-" + i : '';
            events.push({
                event_id: "e" + generation + suffix,
                generation: generation,
                span_id: "s" + generation + suffix,
                transaction: "t" + generation + suffix,
                'transaction.duration': 1234,
                project_id: generation,
                project_slug: "p" + generation,
                parent_event_id: generation === 0 ? null : parentId === null ? "e" + (generation - 1) : parentId,
                parent_span_id: generation === 0
                    ? null
                    : parentId === null
                        ? "s" + (generation - 1) + parentId
                        : "s" + parentId,
            });
        }
        return events;
    }
    function makeTransactionEvent(id) {
        return {
            id: "e" + id,
            type: 'transaction',
            startTimestamp: 1615921516.132774,
            endTimestamp: 1615921517.924861,
        };
    }
    function makeTransactionTarget(pid, eid, transaction, project) {
        var query = { transaction: transaction, project: project };
        return {
            pathname: "/organizations/" + organization.slug + "/performance/" + pid + ":" + eid + "/",
            query: query,
        };
    }
    beforeEach(function () {
        initialize();
        location = {
            pathname: '/',
            query: {},
        };
    });
    describe('Empty Trace', function () {
        it('renders nothing for empty trace', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(1)} quickTrace={{
                    type: 'empty',
                    trace: [],
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            expect(quickTrace.text()).toEqual('\u2014');
        });
    });
    describe('Partial Trace', function () {
        it('renders nothing when partial trace is empty', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(1)} quickTrace={{
                    type: 'partial',
                    trace: null,
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            expect(quickTrace.text()).toEqual('\u2014');
        });
        it('renders nothing when partial trace missing current event', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent('not-1')} quickTrace={{
                    type: 'partial',
                    trace: makeQuickTraceEvents(1),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            expect(quickTrace.text()).toEqual('\u2014');
        });
        it('renders partial trace with no children', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(4)} quickTrace={{
                    type: 'partial',
                    trace: makeQuickTraceEvents(4),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(1);
            expect(nodes.first().text()).toEqual('This Event');
        });
        it('renders partial trace with single child', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(4)} quickTrace={{
                    type: 'partial',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(4))), tslib_1.__read(makeQuickTraceEvents(5))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(2);
            ['This Event', '1 Child'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
        it('renders partial trace with multiple children', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(4)} quickTrace={{
                    type: 'partial',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(4))), tslib_1.__read(makeQuickTraceEvents(5, { n: 3 }))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(2);
            ['This Event', '3 Children'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
        it('renders full trace with root as parent', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(1)} quickTrace={{
                    type: 'partial',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(2);
            ['Parent', 'This Event'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
    });
    describe('Full Trace', function () {
        it('renders full trace with single ancestor', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(3)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))), tslib_1.__read(makeQuickTraceEvents(2))), tslib_1.__read(makeQuickTraceEvents(3))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(4);
            ['Root', '1 Ancestor', 'Parent', 'This Event'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
        it('renders full trace with multiple ancestors', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(5)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))), tslib_1.__read(makeQuickTraceEvents(2))), tslib_1.__read(makeQuickTraceEvents(3))), tslib_1.__read(makeQuickTraceEvents(4))), tslib_1.__read(makeQuickTraceEvents(5))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(4);
            ['Root', '3 Ancestors', 'Parent', 'This Event'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
        it('renders full trace with single descendant', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(0)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))), tslib_1.__read(makeQuickTraceEvents(2))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(3);
            ['This Event', '1 Child', '1 Descendant'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
        it('renders full trace with multiple descendants', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(0)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))), tslib_1.__read(makeQuickTraceEvents(2))), tslib_1.__read(makeQuickTraceEvents(3))), tslib_1.__read(makeQuickTraceEvents(4))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(3);
            ['This Event', '1 Child', '3 Descendants'].forEach(function (text, i) {
                return expect(nodes.at(i).text()).toEqual(text);
            });
        });
        it('renders full trace', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(5)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))), tslib_1.__read(makeQuickTraceEvents(2))), tslib_1.__read(makeQuickTraceEvents(3))), tslib_1.__read(makeQuickTraceEvents(4))), tslib_1.__read(makeQuickTraceEvents(5))), tslib_1.__read(makeQuickTraceEvents(6))), tslib_1.__read(makeQuickTraceEvents(7))), tslib_1.__read(makeQuickTraceEvents(8))), tslib_1.__read(makeQuickTraceEvents(9))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(6);
            ['Root', '3 Ancestors', 'Parent', 'This Event', '1 Child', '3 Descendants'].forEach(function (text, i) { return expect(nodes.at(i).text()).toEqual(text); });
        });
    });
    describe('Event Node Clicks', function () {
        it('renders single event targets', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(3)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1))), tslib_1.__read(makeQuickTraceEvents(2))), tslib_1.__read(makeQuickTraceEvents(3))), tslib_1.__read(makeQuickTraceEvents(4))), tslib_1.__read(makeQuickTraceEvents(5))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var nodes = quickTrace.find('EventNode');
            expect(nodes.length).toEqual(6);
            [
                makeTransactionTarget('p0', 'e0', 't0', '0'),
                makeTransactionTarget('p1', 'e1', 't1', '1'),
                makeTransactionTarget('p2', 'e2', 't2', '2'),
                undefined,
                makeTransactionTarget('p4', 'e4', 't4', '4'),
                makeTransactionTarget('p5', 'e5', 't5', '5'),
            ].forEach(function (target, i) { return expect(nodes.at(i).props().to).toEqual(target); });
        });
        it('renders multiple event targets', function () {
            var quickTrace = enzyme_1.mountWithTheme(<quickTrace_1.default event={makeTransactionEvent(0)} quickTrace={{
                    type: 'full',
                    trace: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(makeQuickTraceEvents(0))), tslib_1.__read(makeQuickTraceEvents(1, { n: 3 }))),
                }} anchor="left" errorDest="issue" transactionDest="performance" location={location} organization={organization}/>);
            var items = quickTrace.find('DropdownItem');
            expect(items.length).toEqual(3);
            // can't easily assert the target is correct since it uses an onClick handler
        });
    });
});
//# sourceMappingURL=quickTrace.spec.jsx.map