Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var scroll_to_element_1 = tslib_1.__importDefault(require("scroll-to-element"));
var utils_1 = require("app/components/events/interfaces/debugMeta/utils");
var packageLink_1 = tslib_1.__importDefault(require("app/components/events/interfaces/packageLink"));
var packageStatus_1 = tslib_1.__importDefault(require("app/components/events/interfaces/packageStatus"));
var togglableAddress_1 = tslib_1.__importDefault(require("app/components/events/interfaces/togglableAddress"));
var types_1 = require("app/components/events/interfaces/types");
var locale_1 = require("app/locale");
var debugMetaStore_1 = require("app/stores/debugMetaStore");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var symbol_1 = tslib_1.__importDefault(require("../symbol"));
var utils_2 = require("../utils");
var expander_1 = tslib_1.__importDefault(require("./expander"));
var groupingBadges_1 = tslib_1.__importDefault(require("./groupingBadges"));
var wrapper_1 = tslib_1.__importDefault(require("./wrapper"));
function Native(_a) {
    var frame = _a.frame, isFrameAfterLastNonApp = _a.isFrameAfterLastNonApp, isExpanded = _a.isExpanded, isHoverPreviewed = _a.isHoverPreviewed, onAddressToggle = _a.onAddressToggle, image = _a.image, includeSystemFrames = _a.includeSystemFrames, showingAbsoluteAddress = _a.showingAbsoluteAddress, showCompleteFunctionName = _a.showCompleteFunctionName, onFunctionNameToggle = _a.onFunctionNameToggle, maxLengthOfRelativeAddress = _a.maxLengthOfRelativeAddress, platform = _a.platform, prevFrame = _a.prevFrame, isPrefix = _a.isPrefix, isSentinel = _a.isSentinel, isUsedForGrouping = _a.isUsedForGrouping, haveFramesAtLeastOneExpandedFrame = _a.haveFramesAtLeastOneExpandedFrame, haveFramesAtLeastOneGroupingBadge = _a.haveFramesAtLeastOneGroupingBadge, props = tslib_1.__rest(_a, ["frame", "isFrameAfterLastNonApp", "isExpanded", "isHoverPreviewed", "onAddressToggle", "image", "includeSystemFrames", "showingAbsoluteAddress", "showCompleteFunctionName", "onFunctionNameToggle", "maxLengthOfRelativeAddress", "platform", "prevFrame", "isPrefix", "isSentinel", "isUsedForGrouping", "haveFramesAtLeastOneExpandedFrame", "haveFramesAtLeastOneGroupingBadge"]);
    var _b = frame !== null && frame !== void 0 ? frame : {}, instructionAddr = _b.instructionAddr, trust = _b.trust, addrMode = _b.addrMode, symbolicatorStatus = _b.symbolicatorStatus;
    function packageStatus() {
        // this is the status of image that belongs to this frame
        if (!image) {
            return 'empty';
        }
        var combinedStatus = utils_1.combineStatus(image.debug_status, image.unwind_status);
        switch (combinedStatus) {
            case 'unused':
                return 'empty';
            case 'found':
                return 'success';
            default:
                return 'error';
        }
    }
    function makeFilter(addr) {
        if (!(!addrMode || addrMode === 'abs') && image) {
            return image.debug_id + "!" + addr;
        }
        return addr;
    }
    function scrollToImage(event) {
        event.stopPropagation(); // to prevent collapsing if collapsable
        if (instructionAddr) {
            debugMetaStore_1.DebugMetaActions.updateFilter(makeFilter(instructionAddr));
        }
        scroll_to_element_1.default('#images-loaded');
    }
    var shouldShowLinkToImage = !!symbolicatorStatus &&
        symbolicatorStatus !== types_1.SymbolicatorStatus.UNKNOWN_IMAGE &&
        !isHoverPreviewed;
    var isInlineFrame = prevFrame &&
        utils_2.getPlatform(frame.platform, platform !== null && platform !== void 0 ? platform : 'other') ===
            (prevFrame.platform || platform) &&
        instructionAddr === prevFrame.instructionAddr;
    var isFoundByStackScanning = trust === 'scan' || trust === 'cfi-scan';
    return (<wrapper_1.default className="title as-table" haveFramesAtLeastOneExpandedFrame={haveFramesAtLeastOneExpandedFrame} haveFramesAtLeastOneGroupingBadge={haveFramesAtLeastOneGroupingBadge}>
      <NativeLineContent isFrameAfterLastNonApp={!!isFrameAfterLastNonApp}>
        <PackageLinkWrapper>
          <packageLink_1.default includeSystemFrames={!!includeSystemFrames} withLeadHint={false} packagePath={frame.package} onClick={scrollToImage} isClickable={shouldShowLinkToImage} isHoverPreviewed={isHoverPreviewed}>
            {!isHoverPreviewed && (<packageStatus_1.default status={packageStatus()} tooltip={locale_1.t('Go to Images Loaded')}/>)}
          </packageLink_1.default>
        </PackageLinkWrapper>
        {instructionAddr && (<togglableAddress_1.default address={instructionAddr} startingAddress={image ? image.image_addr : null} isAbsolute={!!showingAbsoluteAddress} isFoundByStackScanning={isFoundByStackScanning} isInlineFrame={!!isInlineFrame} onToggle={onAddressToggle} relativeAddressMaxlength={maxLengthOfRelativeAddress} isHoverPreviewed={isHoverPreviewed}/>)}
        <symbol_1.default frame={frame} showCompleteFunctionName={!!showCompleteFunctionName} onFunctionNameToggle={onFunctionNameToggle} isHoverPreviewed={isHoverPreviewed}/>
      </NativeLineContent>
      {haveFramesAtLeastOneGroupingBadge && (<groupingBadges_1.default isPrefix={isPrefix} isSentinel={isSentinel} isUsedForGrouping={isUsedForGrouping}/>)}
      <expander_1.default isExpanded={isExpanded} isHoverPreviewed={isHoverPreviewed} platform={platform} {...props}/>
    </wrapper_1.default>);
}
exports.default = Native;
var PackageLinkWrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  order: 2;\n\n  @media (min-width: ", ") {\n    order: 0;\n  }\n"], ["\n  order: 2;\n\n  @media (min-width: ", ") {\n    order: 0;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var NativeLineContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  flex: 1;\n  grid-gap: ", ";\n  grid-template-columns: auto 1fr;\n  align-items: center;\n  justify-content: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n"], ["\n  display: grid;\n  flex: 1;\n  grid-gap: ", ";\n  grid-template-columns: auto 1fr;\n  align-items: center;\n  justify-content: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n"])), space_1.default(0.5), function (props) { return props.theme.breakpoints[0]; }, function (p) { return (p.isFrameAfterLastNonApp ? '200px' : '150px'); }, function (props) { return props.theme.breakpoints[2]; }, function (props) {
    return props.theme.breakpoints[3];
}, function (p) { return (p.isFrameAfterLastNonApp ? '180px' : '140px'); });
var templateObject_1, templateObject_2;
//# sourceMappingURL=native.jsx.map