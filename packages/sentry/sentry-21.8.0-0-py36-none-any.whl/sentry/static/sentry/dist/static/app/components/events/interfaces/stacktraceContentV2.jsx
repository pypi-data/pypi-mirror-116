Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var platformicons_1 = require("platformicons");
var lineV2_1 = tslib_1.__importDefault(require("app/components/events/interfaces/frame/lineV2"));
var utils_1 = require("app/components/events/interfaces/frame/utils");
var utils_2 = require("app/components/events/interfaces/utils");
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function StackTraceContent(_a) {
    var data = _a.data, platform = _a.platform, event = _a.event, newestFirst = _a.newestFirst, className = _a.className, isHoverPreviewed = _a.isHoverPreviewed, groupingCurrentLevel = _a.groupingCurrentLevel, _b = _a.includeSystemFrames, includeSystemFrames = _b === void 0 ? true : _b, _c = _a.expandFirstFrame, expandFirstFrame = _c === void 0 ? true : _c;
    var _d = tslib_1.__read(react_1.useState(false), 2), showingAbsoluteAddresses = _d[0], setShowingAbsoluteAddresses = _d[1];
    var _e = tslib_1.__read(react_1.useState(false), 2), showCompleteFunctionName = _e[0], setShowCompleteFunctionName = _e[1];
    var _f = data.frames, frames = _f === void 0 ? [] : _f, framesOmitted = data.framesOmitted, registers = data.registers;
    function findImageForAddress(address, addrMode) {
        var _a, _b;
        var images = (_b = (_a = event.entries.find(function (entry) { return entry.type === 'debugmeta'; })) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.images;
        return images && address
            ? images.find(function (img, idx) {
                if (!addrMode || addrMode === 'abs') {
                    var _a = tslib_1.__read(utils_2.getImageRange(img), 2), startAddress = _a[0], endAddress = _a[1];
                    return address >= startAddress && address < endAddress;
                }
                return addrMode === "rel:" + idx;
            })
            : null;
    }
    function getClassName() {
        if (includeSystemFrames) {
            return className + " traceback full-traceback";
        }
        return className + " traceback in-app-traceback";
    }
    function handleToggleAddresses(mouseEvent) {
        mouseEvent.stopPropagation(); // to prevent collapsing if collapsable
        setShowingAbsoluteAddresses(!showingAbsoluteAddresses);
    }
    function handleToggleFunctionName(mouseEvent) {
        mouseEvent.stopPropagation(); // to prevent collapsing if collapsable
        setShowCompleteFunctionName(!showCompleteFunctionName);
    }
    function isFrameUsedForGrouping(frame) {
        var minGroupingLevel = frame.minGroupingLevel;
        if (groupingCurrentLevel === undefined || minGroupingLevel === undefined) {
            return false;
        }
        return minGroupingLevel <= groupingCurrentLevel;
    }
    function getFramesDetails() {
        var haveFramesAtLeastOneExpandedFrame = false;
        var haveFramesAtLeastOneGroupingBadge = false;
        for (var frameIndex in frames) {
            var frame = frames[Number(frameIndex)];
            if (!haveFramesAtLeastOneExpandedFrame) {
                haveFramesAtLeastOneExpandedFrame = utils_1.isExpandable({
                    frame: frame,
                    registers: registers !== null && registers !== void 0 ? registers : {},
                    emptySourceNotation: frames.length - 1 === Number(frameIndex) && Number(frameIndex) === 0,
                    platform: platform,
                });
            }
            if (!haveFramesAtLeastOneGroupingBadge) {
                haveFramesAtLeastOneGroupingBadge =
                    isFrameUsedForGrouping(frame) || !!frame.isPrefix || !!frame.isSentinel;
            }
            if (haveFramesAtLeastOneExpandedFrame && haveFramesAtLeastOneGroupingBadge) {
                break;
            }
        }
        return {
            haveFramesAtLeastOneExpandedFrame: haveFramesAtLeastOneExpandedFrame,
            haveFramesAtLeastOneGroupingBadge: haveFramesAtLeastOneGroupingBadge,
        };
    }
    function renderOmittedFrames(firstFrameOmitted, lastFrameOmitted) {
        return (<listItem_1.default className="frame frames-omitted">
        {locale_1.t('Frames %d until %d were omitted and not available.', firstFrameOmitted, lastFrameOmitted)}
      </listItem_1.default>);
    }
    function renderConvertedFrames() {
        var _a, _b;
        var firstFrameOmitted = (_a = framesOmitted === null || framesOmitted === void 0 ? void 0 : framesOmitted[0]) !== null && _a !== void 0 ? _a : null;
        var lastFrameOmitted = (_b = framesOmitted === null || framesOmitted === void 0 ? void 0 : framesOmitted[1]) !== null && _b !== void 0 ? _b : null;
        var lastFrameIndex = frames.length - 1;
        var _c = getFramesDetails(), haveFramesAtLeastOneExpandedFrame = _c.haveFramesAtLeastOneExpandedFrame, haveFramesAtLeastOneGroupingBadge = _c.haveFramesAtLeastOneGroupingBadge;
        var nRepeats = 0;
        var maxLengthOfAllRelativeAddresses = frames.reduce(function (maxLengthUntilThisPoint, frame) {
            var correspondingImage = findImageForAddress(frame.instructionAddr, frame.addrMode);
            try {
                var relativeAddress = (utils_2.parseAddress(frame.instructionAddr) -
                    utils_2.parseAddress(correspondingImage.image_addr)).toString(16);
                return maxLengthUntilThisPoint > relativeAddress.length
                    ? maxLengthUntilThisPoint
                    : relativeAddress.length;
            }
            catch (_a) {
                return maxLengthUntilThisPoint;
            }
        }, 0);
        var convertedFrames = frames
            .map(function (frame, frameIndex) {
            var prevFrame = frames[frameIndex - 1];
            var nextFrame = frames[frameIndex + 1];
            var repeatedFrame = nextFrame &&
                frame.lineNo === nextFrame.lineNo &&
                frame.instructionAddr === nextFrame.instructionAddr &&
                frame.package === nextFrame.package &&
                frame.module === nextFrame.module &&
                frame.function === nextFrame.function;
            if (repeatedFrame) {
                nRepeats++;
            }
            var isUsedForGrouping = isFrameUsedForGrouping(frame);
            var isVisible = includeSystemFrames || frame.inApp || isUsedForGrouping;
            if (isVisible && !repeatedFrame) {
                var lineProps = {
                    event: event,
                    frame: frame,
                    isExpanded: expandFirstFrame && lastFrameIndex === frameIndex,
                    emptySourceNotation: lastFrameIndex === frameIndex && frameIndex === 0,
                    prevFrame: prevFrame,
                    platform: platform,
                    timesRepeated: nRepeats,
                    showingAbsoluteAddress: showingAbsoluteAddresses,
                    onAddressToggle: handleToggleAddresses,
                    image: findImageForAddress(frame.instructionAddr, frame.addrMode),
                    maxLengthOfRelativeAddress: maxLengthOfAllRelativeAddresses,
                    registers: {},
                    includeSystemFrames: includeSystemFrames,
                    onFunctionNameToggle: handleToggleFunctionName,
                    showCompleteFunctionName: showCompleteFunctionName,
                    isHoverPreviewed: isHoverPreviewed,
                    isPrefix: !!frame.isPrefix,
                    isSentinel: !!frame.isSentinel,
                    isUsedForGrouping: isUsedForGrouping,
                    haveFramesAtLeastOneExpandedFrame: haveFramesAtLeastOneExpandedFrame,
                    haveFramesAtLeastOneGroupingBadge: haveFramesAtLeastOneGroupingBadge,
                };
                nRepeats = 0;
                if (frameIndex === firstFrameOmitted) {
                    return (<react_1.Fragment key={frameIndex}>
                <lineV2_1.default {...lineProps}/>
                {renderOmittedFrames(firstFrameOmitted, lastFrameOmitted)}
              </react_1.Fragment>);
                }
                return <lineV2_1.default key={frameIndex} {...lineProps}/>;
            }
            if (!repeatedFrame) {
                nRepeats = 0;
            }
            if (frameIndex !== firstFrameOmitted) {
                return null;
            }
            return renderOmittedFrames(firstFrameOmitted, lastFrameOmitted);
        })
            .filter(function (frame) { return !!frame; });
        if (convertedFrames.length > 0 && registers) {
            var lastFrame = convertedFrames.length - 1;
            convertedFrames[lastFrame] = react_1.cloneElement(convertedFrames[lastFrame], {
                registers: registers,
            });
            if (!newestFirst) {
                return convertedFrames;
            }
            return tslib_1.__spreadArray([], tslib_1.__read(convertedFrames)).reverse();
        }
        if (!newestFirst) {
            return convertedFrames;
        }
        return tslib_1.__spreadArray([], tslib_1.__read(convertedFrames)).reverse();
    }
    return (<Wrapper className={getClassName()}>
      <StyledPlatformIcon platform={utils_2.stackTracePlatformIcon(platform, frames)} size="20px" style={{ borderRadius: '3px 0 0 3px' }}/>
      <StyledList>{renderConvertedFrames()}</StyledList>
    </Wrapper>);
}
exports.default = StackTraceContent;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledPlatformIcon = styled_1.default(platformicons_1.PlatformIcon)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  margin-top: -1px;\n  left: -", ";\n"], ["\n  position: absolute;\n  margin-top: -1px;\n  left: -", ";\n"])), space_1.default(3));
var StyledList = styled_1.default(list_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-gap: 0;\n"], ["\n  grid-gap: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=stacktraceContentV2.jsx.map