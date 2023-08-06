Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var packageStatus_1 = require("app/components/events/interfaces/packageStatus");
var togglableAddress_1 = require("app/components/events/interfaces/togglableAddress");
var strictClick_1 = tslib_1.__importDefault(require("app/components/strictClick"));
var withSentryAppComponents_1 = tslib_1.__importDefault(require("app/utils/withSentryAppComponents"));
var context_1 = tslib_1.__importDefault(require("../context"));
var symbol_1 = require("../symbol");
var utils_1 = require("../utils");
var default_1 = tslib_1.__importDefault(require("./default"));
var native_1 = tslib_1.__importDefault(require("./native"));
function Line(_a) {
    var _b, _c, _d;
    var frame = _a.frame, prevFrame = _a.prevFrame, timesRepeated = _a.timesRepeated, includeSystemFrames = _a.includeSystemFrames, onAddressToggle = _a.onAddressToggle, onFunctionNameToggle = _a.onFunctionNameToggle, showingAbsoluteAddress = _a.showingAbsoluteAddress, showCompleteFunctionName = _a.showCompleteFunctionName, isFrameAfterLastNonApp = _a.isFrameAfterLastNonApp, isSentinel = _a.isSentinel, isUsedForGrouping = _a.isUsedForGrouping, isPrefix = _a.isPrefix, haveFramesAtLeastOneExpandedFrame = _a.haveFramesAtLeastOneExpandedFrame, haveFramesAtLeastOneGroupingBadge = _a.haveFramesAtLeastOneGroupingBadge, maxLengthOfRelativeAddress = _a.maxLengthOfRelativeAddress, image = _a.image, registers = _a.registers, isOnlyFrame = _a.isOnlyFrame, event = _a.event, components = _a.components, _e = _a.emptySourceNotation, emptySourceNotation = _e === void 0 ? false : _e, 
    /**
     * Is the stack trace being previewed in a hovercard?
     */
    _f = _a.isHoverPreviewed, 
    /**
     * Is the stack trace being previewed in a hovercard?
     */
    isHoverPreviewed = _f === void 0 ? false : _f, props = tslib_1.__rest(_a, ["frame", "prevFrame", "timesRepeated", "includeSystemFrames", "onAddressToggle", "onFunctionNameToggle", "showingAbsoluteAddress", "showCompleteFunctionName", "isFrameAfterLastNonApp", "isSentinel", "isUsedForGrouping", "isPrefix", "haveFramesAtLeastOneExpandedFrame", "haveFramesAtLeastOneGroupingBadge", "maxLengthOfRelativeAddress", "image", "registers", "isOnlyFrame", "event", "components", "emptySourceNotation", "isHoverPreviewed"]);
    var _g = tslib_1.__read(react_1.useState((_b = props.isExpanded) !== null && _b !== void 0 ? _b : false), 2), isExpanded = _g[0], setIsExpanded = _g[1];
    /* Prioritize the frame platform but fall back to the platform
     of the stack trace / exception */
    var platform = utils_1.getPlatform(frame.platform, (_c = props.platform) !== null && _c !== void 0 ? _c : 'other');
    var expandable = utils_1.isExpandable({
        frame: frame,
        registers: registers,
        platform: platform,
        emptySourceNotation: emptySourceNotation,
        isOnlyFrame: isOnlyFrame,
    });
    function toggleContext(evt) {
        evt && evt.preventDefault();
        setIsExpanded(!isExpanded);
    }
    function renderLine() {
        switch (platform) {
            case 'objc':
            // fallthrough
            case 'cocoa':
            // fallthrough
            case 'native':
                return (<strictClick_1.default onClick={expandable ? toggleContext : undefined}>
            <native_1.default frame={frame} prevFrame={prevFrame} isHoverPreviewed={isHoverPreviewed} platform={platform} isExpanded={isExpanded} isExpandable={expandable} onAddressToggle={onAddressToggle} onFunctionNameToggle={onFunctionNameToggle} includeSystemFrames={includeSystemFrames} showingAbsoluteAddress={showingAbsoluteAddress} showCompleteFunctionName={showCompleteFunctionName} isFrameAfterLastNonApp={isFrameAfterLastNonApp} onToggleContext={toggleContext} isSentinel={isSentinel} isPrefix={isPrefix} isUsedForGrouping={isUsedForGrouping} haveFramesAtLeastOneExpandedFrame={haveFramesAtLeastOneExpandedFrame} haveFramesAtLeastOneGroupingBadge={haveFramesAtLeastOneGroupingBadge} image={image} maxLengthOfRelativeAddress={maxLengthOfRelativeAddress}/>
          </strictClick_1.default>);
            default:
                return (<strictClick_1.default onClick={expandable ? toggleContext : undefined}>
            <default_1.default frame={frame} timesRepeated={timesRepeated} isHoverPreviewed={isHoverPreviewed} platform={platform} isExpanded={isExpanded} isExpandable={expandable} onToggleContext={toggleContext} isSentinel={isSentinel} isPrefix={isPrefix} isUsedForGrouping={isUsedForGrouping} haveFramesAtLeastOneExpandedFrame={haveFramesAtLeastOneExpandedFrame} haveFramesAtLeastOneGroupingBadge={haveFramesAtLeastOneGroupingBadge}/>
          </strictClick_1.default>);
        }
    }
    var className = classnames_1.default({
        frame: true,
        'is-expandable': expandable,
        expanded: isExpanded,
        collapsed: !isExpanded,
        'system-frame': !frame.inApp,
        'frame-errors': !!((_d = frame.errors) !== null && _d !== void 0 ? _d : []).length,
    });
    return (<StyledLi className={className}>
      {renderLine()}
      <context_1.default frame={frame} event={event} registers={registers} components={components} hasContextSource={utils_1.hasContextSource(frame)} hasContextVars={utils_1.hasContextVars(frame)} hasContextRegisters={utils_1.hasContextRegisters(registers)} emptySourceNotation={emptySourceNotation} hasAssembly={utils_1.hasAssembly(frame, platform)} expandable={expandable} isExpanded={isExpanded}/>
    </StyledLi>);
}
exports.default = withSentryAppComponents_1.default(Line, { componentType: 'stacktrace-link' });
var StyledLi = styled_1.default('li')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n\n  ", " {\n    flex-shrink: 0;\n  }\n  :hover {\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n  }\n"], ["\n  overflow: hidden;\n\n  ", " {\n    flex-shrink: 0;\n  }\n  :hover {\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n  }\n"])), packageStatus_1.PackageStatusIcon, packageStatus_1.PackageStatusIcon, togglableAddress_1.AddressToggleIcon, symbol_1.FunctionNameToggleIcon);
var templateObject_1;
//# sourceMappingURL=index.jsx.map