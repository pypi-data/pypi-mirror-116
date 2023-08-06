Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var crashContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashContent"));
var crashActions_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashActions"));
var crashTitle_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashHeader/crashTitle"));
var stacktrace_1 = require("app/components/events/interfaces/stacktrace");
var locale_1 = require("app/locale");
var stacktrace_2 = require("app/types/stacktrace");
var utils_1 = require("app/utils");
function Exception(_a) {
    var event = _a.event, type = _a.type, data = _a.data, projectId = _a.projectId, hasGroupingTreeUI = _a.hasGroupingTreeUI, groupingCurrentLevel = _a.groupingCurrentLevel, _b = _a.hideGuide, hideGuide = _b === void 0 ? false : _b;
    var _c = tslib_1.__read(react_1.useState(data.hasSystemFrames ? stacktrace_2.STACK_VIEW.APP : stacktrace_2.STACK_VIEW.FULL), 2), stackView = _c[0], setStackView = _c[1];
    var _d = tslib_1.__read(react_1.useState(stacktrace_2.STACK_TYPE.ORIGINAL), 2), stackType = _d[0], setStackType = _d[1];
    var _e = tslib_1.__read(react_1.useState(stacktrace_1.isStacktraceNewestFirst()), 2), newestFirst = _e[0], setNewestFirst = _e[1];
    var eventHasThreads = !!event.entries.find(function (entry) { return entry.type === 'threads'; });
    /* in case there are threads in the event data, we don't render the
     exception block.  Instead the exception is contained within the
     thread interface. */
    if (eventHasThreads) {
        return null;
    }
    function handleChange(_a) {
        var newStackView = _a.stackView, newStackType = _a.stackType, newNewestFirst = _a.newestFirst;
        if (newStackView) {
            setStackView(newStackView);
        }
        if (utils_1.defined(newNewestFirst)) {
            setNewestFirst(newNewestFirst);
        }
        if (newStackType) {
            setStackType(newStackType);
        }
    }
    var commonCrashHeaderProps = {
        newestFirst: newestFirst,
        hideGuide: hideGuide,
        onChange: handleChange,
    };
    return (<eventDataSection_1.default type={type} title={<crashTitle_1.default title={locale_1.t('Exception')} {...commonCrashHeaderProps}/>} actions={<crashActions_1.default stackType={stackType} stackView={stackView} platform={event.platform} exception={data} hasGroupingTreeUI={hasGroupingTreeUI} {...commonCrashHeaderProps}/>} wrapTitle={false}>
      <crashContent_1.default projectId={projectId} event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} exception={data} hasGroupingTreeUI={hasGroupingTreeUI} groupingCurrentLevel={groupingCurrentLevel}/>
    </eventDataSection_1.default>);
}
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map